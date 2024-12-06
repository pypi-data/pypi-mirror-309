use pyo3::prelude::*;
use ironfish::keys::PublicAddress;

#[pyfunction]
fn validate_address(address: &str) -> PyResult<bool> {
    Ok(PublicAddress::from_hex(address).is_ok())
}

#[pymodule]
fn pyironfish(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate_address, m)?)?;
    Ok(())
}
