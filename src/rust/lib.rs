//! TS-Core Rust kernel — persistent wave engine (Kernel Wave 12 path).
//! Links `kernel`, `bindings` (optional PyO3), and shared `wave_propagate`.

pub mod kernel;

#[path = "../shared/wave_propagate.rs"]
pub mod wave_propagate;

#[cfg(feature = "python")]
pub mod bindings;

pub use kernel::{KernelConfig, KernelPhase, TsKernel};
pub use wave_propagate::{propagate_wave_step, WaveEdge, WaveGraph, WaveNode};

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pymodule]
fn ts_core_kernel(m: &Bound<'_, PyModule>) -> PyResult<()> {
    bindings::register(m)
}
