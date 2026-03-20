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

// --- Kernel Wave 12 (Pages Island): 9-phase native-TS OS tick ----------------

/// Global tension (activation RMS deviation) for any graph.
pub fn measure_tension_graph(g: &WaveGraph) -> f64 {
    let vals: Vec<f64> = g.nodes.values().map(|n| n.activation).collect();
    if vals.is_empty() {
        return 0.0;
    }
    let m = vals.iter().sum::<f64>() / vals.len() as f64;
    let v = vals.iter().map(|x| (x - m).powi(2)).sum::<f64>() / vals.len() as f64;
    v.sqrt()
}

#[derive(Debug, Clone)]
pub struct Wave12Trace {
    pub phases: Vec<String>,
    pub strongest: String,
    pub tension_before: f64,
    pub tension_after: f64,
    pub validation_ok: bool,
}

/// Kernel Wave 12 scheduler: one OS-level quantum = phases 1–9 on the strongest-node wave.
/// No traditional priority scheduler — the strongest stable activation leads the spin.
pub struct Wave12Scheduler;

impl Wave12Scheduler {
    /// Phases 1–3: strongest-node detection, lock, initial spin.
    /// Phases 4–6: constraint propagation (process / resource / surge) via damped waves.
    /// Phases 7–9: Icarus seal on wax-wing nodes, self-validation, Pages Island persist marker.
    pub fn apply(graph: &mut WaveGraph, damping: f64) -> Wave12Trace {
        let mut phases: Vec<String> = Vec::new();
        let d = damping.clamp(0.0, 1.0);
        let t0 = measure_tension_graph(graph);

        // Phase 1: strongest-node scan (activation * stability)
        let strongest = graph
            .nodes
            .iter()
            .max_by(|(_, a), (_, b)| {
                let sa = a.activation * a.stability;
                let sb = b.activation * b.stability;
                sa.total_cmp(&sb)
            })
            .map(|(id, _)| id.clone())
            .unwrap_or_default();
        phases.push(format!("1_strongest_scan:{strongest}"));

        // Phase 2: lock / bias strongest (initial scheduling decision = native TS, not FIFO)
        if let Some(n) = graph.nodes.get_mut(&strongest) {
            n.activation = (n.activation + 0.035).min(1.0);
            n.stability = (n.stability + 0.01).min(1.0);
        }
        phases.push("2_strongest_lock_spin_budget".into());

        // Phase 3: initial spin — first relaxation after bias
        propagate_wave_step(graph, (d * 1.12).min(1.0));
        phases.push("3_initial_spin".into());

        // Phases 4–6: cross-cutting constraint propagation (process, resource, surge)
        propagate_wave_step(graph, d);
        phases.push("4_process_fanout".into());
        propagate_wave_step(graph, d);
        phases.push("5_resource_coupling".into());
        propagate_wave_step(graph, d);
        phases.push("6_constraint_surge".into());

        // Phase 7: Icarus seal — low-stability “wax” nodes cannot dominate activation
        if !graph.nodes.is_empty() {
            let mean_act =
                graph.nodes.values().map(|n| n.activation).sum::<f64>() / graph.nodes.len() as f64;
            for n in graph.nodes.values_mut() {
                if n.stability < 0.18 {
                    n.activation = (n.activation * 0.65 + mean_act * 0.35).clamp(0.0, 1.0);
                }
            }
        }
        phases.push("7_icarus_wings_seal".into());

        let t_mid = measure_tension_graph(graph);

        // Phase 8: self-validation — OS-level fireproof check (no runaway narrative tension)
        phases.push(format!(
            "8_self_validation:tension_mid={t_mid:.6}"
        ));

        // Phase 9: Pages Island persistence tick (logical commit; host I/O in Python)
        propagate_wave_step(graph, d * 0.85);
        let t1 = measure_tension_graph(graph);
        phases.push(format!(
            "9_pages_island_persist:tension_final={t1:.6}"
        ));

        let validation_ok = t1.is_finite() && t1 <= t0 + 0.12;

        Wave12Trace {
            phases,
            strongest,
            tension_before: t0,
            tension_after: t1,
            validation_ok,
        }
    }
}
