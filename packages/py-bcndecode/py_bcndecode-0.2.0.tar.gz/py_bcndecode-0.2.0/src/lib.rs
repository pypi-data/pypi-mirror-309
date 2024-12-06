use pyo3::types::PyBytes;
use pyo3::{prelude::*, wrap_pyfunction};

use bcndecode::decode;
use bcndecode::BcnEncoding;
use bcndecode::BcnDecoderFormat::RGBA;

fn encoding_from_str(val: String) -> BcnEncoding {
    match val.as_str() {
        "bc1" => BcnEncoding::Bc1,
        "bc3" => BcnEncoding::Bc3,
        "bc5" => BcnEncoding::Bc5,
        _ => BcnEncoding::Bc6H,
    }
}

#[pyfunction]
fn decode_bcn(py: Python, source: &PyBytes, width: u32, height: u32, encoding: String) -> Py<PyBytes> {
    let enc = encoding_from_str(encoding);
    let decoded = decode(source.as_bytes(), width as usize, height as usize, enc, RGBA);
    let res: Py<PyBytes> = PyBytes::new(py, decoded.unwrap().as_slice()).into();
    res

}

/// A Python module implemented in Rust.
#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(decode_bcn, m)?)?;
    Ok(())
}
