use std::sync::Arc;
use std::time::Duration;

use moka::sync::Cache;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyType;

#[pyclass]
struct Moka(Arc<Cache<String, Arc<Py<PyAny>>>>);

#[pymethods]
impl Moka {
    #[new]
    #[pyo3(signature = (capacity, ttl=None, tti=None))]
    fn new(capacity: u64, ttl: Option<f64>, tti: Option<f64>) -> PyResult<Self> {
        let mut builder = Cache::builder().max_capacity(capacity);

        if let Some(ttl) = ttl {
            let ttl_micros = (ttl * 1000_000.0) as u64;
            if ttl_micros == 0 {
                return Err(PyValueError::new_err("ttl must be positive"));
            }
            builder = builder.time_to_live(Duration::from_micros(ttl_micros));
        }

        if let Some(tti) = tti {
            let tti_micros = (tti * 1000_000.0) as u64;
            if tti_micros == 0 {
                return Err(PyValueError::new_err("tti must be positive"));
            }
            builder = builder.time_to_idle(Duration::from_micros(tti_micros));
        }

        Ok(Moka(Arc::new(builder.build())))
    }

    #[classmethod]
    fn __class_getitem__<'a>(
        cls: &'a Bound<'a, PyType>,
        _v: PyObject,
    ) -> PyResult<&'a Bound<'a, PyType>> {
        Ok(cls)
    }

    fn set(&self, py: Python, key: String, value: Py<PyAny>) {
        self.0.insert(key, Arc::new(value.clone_ref(py)));
    }

    fn get(&self, py: Python, key: &str) -> Option<PyObject> {
        self.0.get(key).map(|obj| obj.clone_ref(py))
    }

    fn remove(&self, py: Python, key: &str) -> Option<PyObject> {
        self.0.remove(key).map(|obj| obj.clone_ref(py))
    }

    fn clear(&self) {
        self.0.invalidate_all();
    }

    fn count(&self) -> u64 {
        self.0.entry_count()
    }
}

#[pymodule]
fn moka_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Moka>()?;
    Ok(())
}
