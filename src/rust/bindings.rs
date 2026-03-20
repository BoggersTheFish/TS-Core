//! PyO3 bindings — `maturin develop --features python` to load from Python.
//! The persistent wave with Grok and the Architect's fireproof TS wings.

use crate::wave_propagate::{propagate_wave_step, WaveEdge, WaveGraph, WaveNode};
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::types::PyList;

fn graph_from_pydict(dict: &Bound<'_, PyDict>) -> PyResult<WaveGraph> {
    let mut g = WaveGraph::default();
    let nodes_any = dict
        .get_item("nodes")?
        .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("missing nodes"))?;
    let nodes = nodes_any.downcast::<PyDict>()?;
    for (k, v) in nodes.iter() {
        let id: String = k.extract()?;
        let nobj = v.downcast::<PyDict>()?;
        let activation: f64 = nobj
            .get_item("activation")?
            .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("activation"))?
            .extract()?;
        let stability: f64 = nobj
            .get_item("stability")?
            .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("stability"))?
            .extract()?;
        g.nodes.insert(
            id.clone(),
            WaveNode {
                id,
                activation,
                stability,
            },
        );
    }
    let edges_any = dict
        .get_item("edges")?
        .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("missing edges"))?;
    let list = edges_any.downcast::<PyList>()?;
    for item in list.iter() {
        let e = item.downcast::<PyDict>()?;
        let from: String = e
            .get_item("from")?
            .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("from"))?
            .extract()?;
        let to: String = e
            .get_item("to")?
            .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("to"))?
            .extract()?;
        let weight: f64 = e
            .get_item("weight")?
            .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("weight"))?
            .extract()?;
        g.edges.push(WaveEdge { from, to, weight });
    }
    Ok(g)
}

fn graph_to_pydict(py: Python<'_>, g: &WaveGraph) -> PyResult<Py<PyDict>> {
    let out = PyDict::new_bound(py);
    let nodes = PyDict::new_bound(py);
    for (id, n) in &g.nodes {
        let nd = PyDict::new_bound(py);
        nd.set_item("activation", n.activation)?;
        nd.set_item("stability", n.stability)?;
        nodes.set_item(id, nd)?;
    }
    out.set_item("nodes", nodes)?;
    let edges = PyList::empty_bound(py);
    for e in &g.edges {
        let ed = PyDict::new_bound(py);
        ed.set_item("from", &e.from)?;
        ed.set_item("to", &e.to)?;
        ed.set_item("weight", e.weight)?;
        edges.append(ed)?;
    }
    out.set_item("edges", edges)?;
    Ok(out.unbind())
}

#[pyfunction]
fn rust_propagate_wave(py: Python<'_>, graph_dict: Bound<'_, PyDict>, damping: f64) -> PyResult<Py<PyDict>> {
    let mut g = graph_from_pydict(&graph_dict)?;
    propagate_wave_step(&mut g, damping);
    graph_to_pydict(py, &g)
}

#[pyfunction]
fn rust_wave_tension(graph_dict: Bound<'_, PyDict>) -> PyResult<f64> {
    let g = graph_from_pydict(&graph_dict)?;
    let vals: Vec<f64> = g.nodes.values().map(|n| n.activation).collect();
    if vals.is_empty() {
        return Ok(0.0);
    }
    let m = vals.iter().sum::<f64>() / vals.len() as f64;
    let v = vals.iter().map(|x| (x - m).powi(2)).sum::<f64>() / vals.len() as f64;
    Ok(v.sqrt())
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_propagate_wave, m)?)?;
    m.add_function(wrap_pyfunction!(rust_wave_tension, m)?)?;
    Ok(())
}
