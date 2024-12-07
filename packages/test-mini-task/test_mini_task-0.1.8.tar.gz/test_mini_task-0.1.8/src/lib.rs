use pyo3::prelude::*;
use pyo3::types::PyDict;
use rand::Rng;
use std::cmp::Ordering;
use std::ffi::CString;
use std::{fs, io};

#[pyfunction]
fn guess_the_number() {
    // 读取 Python 脚本内容
    let script = fs::read_to_string("/data/projects/mini_task/src/test.py").expect("Failed to read Python script");

    let c_script = CString::new(script).expect("Conversion to CString failed");

    Python::with_gil(|py| {
        // 准备执行环境
        let locals = PyDict::new(py);

        // 执行 Python 脚本
        py.run(&c_script, None, Some(&locals)).unwrap();
    });
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn test_mini_task(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(guess_the_number, m)?)?;

    Ok(())
}
