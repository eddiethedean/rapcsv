use pyo3::prelude::*;
use pyo3_asyncio::tokio::future_into_py;
use tokio::fs::File;
use tokio::fs::OpenOptions;
use tokio::io::{AsyncReadExt, AsyncWriteExt, BufReader};
use csv::ReaderBuilder;

/// Python bindings for rapcsv - Streaming async CSV.
#[pymodule]
fn _rapcsv(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Reader>()?;
    m.add_class::<Writer>()?;
    Ok(())
}

/// Async CSV reader.
#[pyclass]
struct Reader {
    path: String,
    position: usize,
}

#[pymethods]
impl Reader {
    /// Open a CSV file for reading.
    #[new]
    fn new(path: String) -> Self {
        Reader { path, position: 0 }
    }

    /// Read the next row from the CSV file.
    fn read_row(self_: PyRef<Self>) -> PyResult<PyObject> {
        let path = self_.path.clone();
        let position = self_.position;
        Python::with_gil(|py| {
            let future = async move {
                let file = File::open(&path)
                    .await
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("Failed to open file: {}", e)))?;
                
                let mut reader = BufReader::new(file);
                let mut buffer = String::new();
                let mut lines = Vec::new();
                
                // Read file (simplified for MVP - read all at once)
                reader.read_to_string(&mut buffer)
                    .await
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("Failed to read file: {}", e)))?;
                
                let mut csv_reader = ReaderBuilder::new()
                    .has_headers(false)
                    .from_reader(buffer.as_bytes());
                
                for (i, result) in csv_reader.records().enumerate() {
                    if i < position {
                        continue;
                    }
                    match result {
                        Ok(record) => {
                            let row: Vec<String> = record.iter().map(|s| s.to_string()).collect();
                            lines.push(row);
                            break; // Just return one row for MVP
                        }
                        Err(e) => {
                            return Err(PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("CSV parse error: {}", e)));
                        }
                    }
                }
                
                if lines.is_empty() {
                    Ok(Vec::<String>::new()) // EOF
                } else {
                    Ok(lines[0].clone())
                }
            };
            future_into_py(py, future).map(|awaitable| awaitable.to_object(py))
        })
    }
}

/// Async CSV writer.
#[pyclass]
struct Writer {
    path: String,
}

#[pymethods]
impl Writer {
    /// Create a new CSV file for writing.
    #[new]
    fn new(path: String) -> Self {
        Writer { path }
    }

    /// Write a row to the CSV file.
    fn write_row(self_: PyRef<Self>, row: Vec<String>) -> PyResult<PyObject> {
        let path = self_.path.clone();
        Python::with_gil(|py| {
            let future = async move {
                use tokio::fs::OpenOptions;
                // Append mode - creates file if it doesn't exist
                let mut file = OpenOptions::new()
                    .create(true)
                    .append(true)
                    .open(&path)
                    .await
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("Failed to open file: {}", e)))?;
                
                // Simple CSV writing for MVP
                let line = row.join(",") + "\n";
                file.write_all(line.as_bytes())
                    .await
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("Failed to write file: {}", e)))?;
                
                // Flush to ensure data is written
                file.flush()
                    .await
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("Failed to flush file: {}", e)))?;
                
                Ok(())
            };
            future_into_py(py, future).map(|awaitable| awaitable.to_object(py))
        })
    }
}
