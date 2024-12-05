use plane_partition::{cardinality as card, is_plane_partition as is_pp, complement::complement as comp, rowmotion::{find_orbit, find_orbit_length, rowmotion as rowmotion_crate}, strongly_stable_to_totally_stable, PlanePartition};
use pyo3::{exceptions::PyIndexError, prelude::*};

pub mod plane_partition;

/// Prints the package version
#[pyfunction]
fn version() -> PyResult<String> {
    Ok(env!("CARGO_PKG_VERSION").to_string())
}

/// Returns a string that represents the tikz diagram of a plane partition
/// ```python
/// import plane_partitions as pp
/// pp.to_tikz_diagram([[2,1],[1,0]])
/// ```
#[pyfunction]
fn to_tikz_diagram(matrix: Vec<Vec<u8>>) -> PyResult<String> {
    Ok(format!(
        "{}",
        PlanePartition {
            len: 0,
            data: matrix
        }
    ))
}

/// Takes in a strongly stable plane partition and returns a totally symetric plane partition
/// ```py
/// import plane_partitions as pp
/// pp.sspp_tp_tspp([[2,1],[1,0]])
/// # returns [[2,2],[2,2]]
/// ```
#[pyfunction]
fn sspp_tp_tspp(matrix: Vec<Vec<u8>>) -> PyResult<Vec<Vec<u8>>> {
    if matrix.len() != matrix[0].len() {
        return Err(PyErr::new::<PyIndexError, &str>("not a a valid n x n list"));
    }
    Ok(strongly_stable_to_totally_stable(&PlanePartition {
        len: matrix.len(),
        data: matrix,
    })
    .data)
}

/// Takes in a plane partition and returns the resulting plane partition under the action of rowmotion
/// ```py
/// import plane_partitions as pp
/// pp.rowmotion([[0,0],[0,0]])
/// # returns [[1,0],[0,0]]
/// ```
#[pyfunction]
fn rowmotion(matrix: Vec<Vec<u8>>) -> PyResult<Vec<Vec<u8>>> {
    if matrix.len() != matrix[0].len() {
        return Err(PyErr::new::<PyIndexError, &str>("not a a valid n x n list"));
    }
    Ok(rowmotion_crate(&PlanePartition {
        len: matrix.len(),
        data: matrix
    }).data)
}

/// Returns the cardinality of a plane partition
#[pyfunction]
fn cardinality(matrix: Vec<Vec<u8>>) -> PyResult<usize> {
    Ok(card(&PlanePartition {
        len: matrix.len(),
        data: matrix
    }))
}

/// Returns the length of the orbit of a plane partition under rowmotion
/// Should be more efficient than finding the whole orbit instead of just the length
#[pyfunction]
fn rowmotion_orbit_length(matrix: Vec<Vec<u8>>) -> PyResult<usize> {
    if matrix.len() != matrix[0].len() {
        return Err(PyErr::new::<PyIndexError, &str>("not a a valid n x n list"));
    }
    Ok(find_orbit_length(&PlanePartition {
        len: matrix.len(),
        data: matrix
    }))
}

/// Returns the list of all partitions in an orbit of a plane partition under rowmotion
#[pyfunction]
fn rowmotion_orbit(matrix: Vec<Vec<u8>>) -> PyResult<Vec<Vec<Vec<u8>>>> {
    if matrix.len() != matrix[0].len() {
        return Err(PyErr::new::<PyIndexError, &str>("not a a valid n x n list"));
    }
    Ok(find_orbit(&PlanePartition {
        len: matrix.len(),
        data: matrix
    }))
}

/// Returns whether a list of lists is a valid plane partition 
#[pyfunction]
fn is_plane_partition(matrix: Vec<Vec<u8>>) -> PyResult<bool> {
    if matrix.len() != matrix[0].len() {
        return Err(PyErr::new::<PyIndexError, &str>("not a a valid n x n list"));
    }
    Ok(is_pp(&PlanePartition {
        len: matrix.len(),
        data: matrix
    }))
}

/// Finds the complement of a plane partition
#[pyfunction]
fn complement(matrix: Vec<Vec<u8>>) -> PyResult<Vec<Vec<u8>>> {
    if matrix.len() != matrix[0].len() {
        return Err(PyErr::new::<PyIndexError, &str>("not a a valid n x n list"));
    }
    Ok(comp(&PlanePartition {
        len: matrix.len(),
        data: matrix
    }).data)
}

///Python module for working with plane plane partitions
///Written by Jimmy Ostler <jtostler1@gmail.com>
#[pymodule]
fn plane_partitions(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add_function(wrap_pyfunction!(sspp_tp_tspp, m)?)?;
    m.add_function(wrap_pyfunction!(to_tikz_diagram, m)?)?;
    m.add_function(wrap_pyfunction!(rowmotion, m)?)?;
    m.add_function(wrap_pyfunction!(cardinality, m)?)?;
    m.add_function(wrap_pyfunction!(rowmotion_orbit_length, m)?)?;
    m.add_function(wrap_pyfunction!(rowmotion_orbit, m)?)?;
    m.add_function(wrap_pyfunction!(is_plane_partition, m)?)?;
    m.add_function(wrap_pyfunction!(complement, m)?)?;
    Ok(())
}
