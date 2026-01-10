use pyo3::prelude::*;

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
    // TODO: Implement async CSV reader
}

#[pymethods]
impl Reader {
    #[new]
    fn new(path: String) -> PyResult<Self> {
        // TODO: Implement async CSV reader initialization
        Ok(Reader {})
    }

    fn read_row(&mut self) -> PyResult<Vec<String>> {
        // TODO: Implement async CSV row reading
        Ok(vec![])
    }
}

/// Async CSV writer.
#[pyclass]
struct Writer {
    // TODO: Implement async CSV writer
}

#[pymethods]
impl Writer {
    #[new]
    fn new(path: String) -> PyResult<Self> {
        // TODO: Implement async CSV writer initialization
        Ok(Writer {})
    }

    fn write_row(&mut self, row: Vec<String>) -> PyResult<()> {
        // TODO: Implement async CSV row writing
        Ok(())
    }
}

