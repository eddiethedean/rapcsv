#![allow(non_local_definitions)] // False positive from pyo3 macros

use csv::{ReaderBuilder, WriterBuilder};
use pyo3::prelude::*;
use pyo3_async_runtimes::tokio::future_into_py;
use std::sync::Arc;
use tokio::fs::File;
use tokio::io::{AsyncReadExt, AsyncWriteExt, BufReader};
use tokio::sync::Mutex;

/// Validate a file path for security and correctness.
fn validate_path(path: &str) -> PyResult<()> {
    if path.is_empty() {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "Path cannot be empty",
        ));
    }
    if path.contains('\0') {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "Path cannot contain null bytes",
        ));
    }
    Ok(())
}

/// Python bindings for rapcsv - Streaming async CSV.
#[pymodule]
fn _rapcsv(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Reader>()?;
    m.add_class::<Writer>()?;
    Ok(())
}

/// Async CSV reader.
#[pyclass]
struct Reader {
    path: String,
    position: Arc<Mutex<usize>>,
}

#[pymethods]
impl Reader {
    /// Open a CSV file for reading.
    #[new]
    fn new(path: String) -> PyResult<Self> {
        validate_path(&path)?;
        Ok(Reader {
            path,
            position: Arc::new(Mutex::new(0)),
        })
    }

    /// Read the next row from the CSV file.
    fn read_row(self_: PyRef<Self>) -> PyResult<Py<PyAny>> {
        let path = self_.path.clone();
        let position = Arc::clone(&self_.position);
        Python::attach(|py| {
            let future = async move {
                let file = File::open(&path).await.map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "Failed to open file {}: {e}",
                        path
                    ))
                })?;

                let mut reader = BufReader::new(file);
                let mut buffer = String::new();
                let mut lines = Vec::new();

                // Read file (simplified for MVP - read all at once)
                reader.read_to_string(&mut buffer).await.map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "Failed to read file {}: {e}",
                        path
                    ))
                })?;

                let mut csv_reader = ReaderBuilder::new()
                    .has_headers(false)
                    .from_reader(buffer.as_bytes());

                // Get current position
                let current_pos = {
                    let pos_guard = position.lock().await;
                    *pos_guard
                };

                let mut found_row = false;
                let mut found_position = current_pos;

                for (i, result) in csv_reader.records().enumerate() {
                    if i < current_pos {
                        continue;
                    }
                    match result {
                        Ok(record) => {
                            let row: Vec<String> = record.iter().map(|s| s.to_string()).collect();
                            lines.push(row);
                            found_position = i + 1; // Update to next position
                            found_row = true;
                            break; // Just return one row for MVP
                        }
                        Err(e) => {
                            return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                                "CSV parse error at row {}: {e}",
                                i
                            )));
                        }
                    }
                }

                // Update position if we found a row
                if found_row {
                    let mut pos_guard = position.lock().await;
                    *pos_guard = found_position;
                }

                if lines.is_empty() {
                    Ok(Vec::<String>::new()) // EOF
                } else {
                    Ok(lines[0].clone())
                }
            };
            future_into_py(py, future).map(|bound| bound.unbind())
        })
    }
}

/// Async CSV writer.
#[pyclass]
struct Writer {
    path: String,
    file: Arc<Mutex<Option<File>>>,
}

#[pymethods]
impl Writer {
    /// Create a new CSV file for writing.
    #[new]
    fn new(path: String) -> PyResult<Self> {
        validate_path(&path)?;
        Ok(Writer {
            path,
            file: Arc::new(Mutex::new(None)),
        })
    }

    /// Write a row to the CSV file.
    fn write_row(self_: PyRef<Self>, row: Vec<String>) -> PyResult<Py<PyAny>> {
        let path = self_.path.clone();
        let file = Arc::clone(&self_.file);
        Python::attach(|py| {
            let future = async move {
                // Get or open the file handle
                let mut file_guard = file.lock().await;
                if file_guard.is_none() {
                    use tokio::fs::OpenOptions;
                    // Append mode - creates file if it doesn't exist
                    *file_guard = Some(
                        OpenOptions::new()
                            .create(true)
                            .append(true)
                            .open(&path)
                            .await
                            .map_err(|e| {
                                PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                                    "Failed to open file {}: {e}",
                                    path
                                ))
                            })?,
                    );
                }
                let file_ref = file_guard.as_mut().unwrap();

                // Proper CSV writing with escaping and quoting (RFC 4180 compliant)
                let mut writer = WriterBuilder::new()
                    .has_headers(false)
                    .from_writer(Vec::new());
                writer.write_record(&row).map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "Failed to write CSV record: {e}"
                    ))
                })?;
                writer.flush().map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "Failed to flush CSV writer: {e}"
                    ))
                })?;
                let csv_data = writer.into_inner().map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "Failed to finalize CSV record: {e}"
                    ))
                })?;
                file_ref.write_all(&csv_data).await.map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "Failed to write file {}: {e}",
                        path
                    ))
                })?;

                // Flush to ensure data is written
                file_ref.flush().await.map_err(|e| {
                    PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                        "Failed to flush file {}: {e}",
                        path
                    ))
                })?;

                Ok(())
            };
            future_into_py(py, future).map(|bound| bound.unbind())
        })
    }
}
