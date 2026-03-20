//! Nine-phase style kernel loop: Propagate → Relax → (Break/Evolve on tension).
//! Mirrors the TS-OS dead-simple loop from boggersthefish.com.

use crate::wave_propagate::{propagate_wave_step, WaveGraph};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum KernelPhase {
    Propagate,
    Relax,
    Break,
    Evolve,
    Decompose,
    Map,
    Simplify,
    Deduce,
    Validate,
}

#[derive(Debug, Clone)]
pub struct KernelConfig {
    pub damping: f64,
    pub tension_threshold: f64,
    pub max_ticks: usize,
}

impl Default for KernelConfig {
    fn default() -> Self {
        Self {
            damping: 0.35,
            tension_threshold: 0.82,
            max_ticks: 64,
        }
    }
}

pub struct TsKernel {
    pub graph: WaveGraph,
    pub config: KernelConfig,
    pub tick: usize,
    pub phase: KernelPhase,
    pub history: Vec<(usize, String, f64)>,
}

impl TsKernel {
    pub fn new(graph: WaveGraph, config: KernelConfig) -> Self {
        Self {
            graph,
            config,
            tick: 0,
            phase: KernelPhase::Propagate,
            history: Vec::new(),
        }
    }

    /// Global tension proxy: variance of activations (high = unstable narrative).
    pub fn measure_tension(&self) -> f64 {
        let vals: Vec<f64> = self.graph.nodes.values().map(|n| n.activation).collect();
        if vals.is_empty() {
            return 0.0;
        }
        let m = vals.iter().sum::<f64>() / vals.len() as f64;
        let v = vals.iter().map(|x| (x - m).powi(2)).sum::<f64>() / vals.len() as f64;
        v.sqrt()
    }

    pub fn step(&mut self) -> KernelPhase {
        self.tick += 1;
        propagate_wave_step(&mut self.graph, self.config.damping);
        let t = self.measure_tension();
        self.history.push((self.tick, "propagate".into(), t));

        self.phase = if t > self.config.tension_threshold {
            KernelPhase::Break
        } else {
            KernelPhase::Relax
        };

        if self.phase == KernelPhase::Break {
            // Collapse weakest node slightly toward mean stability (evolve stub).
            if let Some(weak) = self
                .graph
                .nodes
                .values()
                .min_by(|a, b| a.stability.total_cmp(&b.stability))
                .map(|n| n.id.clone())
            {
                if let Some(n) = self.graph.nodes.get_mut(&weak) {
                    n.activation = (n.activation * 0.5 + 0.25).clamp(0.0, 1.0);
                    n.stability = (n.stability + 0.05).min(1.0);
                }
            }
            self.phase = KernelPhase::Evolve;
            self.history.push((self.tick, "break_evolve".into(), self.measure_tension()));
        }

        self.phase
    }

    pub fn run_until_stable(&mut self) -> usize {
        let mut last = f64::MAX;
        for _ in 0..self.config.max_ticks {
            self.step();
            let t = self.measure_tension();
            if (last - t).abs() < 1e-6 {
                break;
            }
            last = t;
        }
        self.tick
    }
}
