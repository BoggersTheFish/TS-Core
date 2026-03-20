//! Native TS wave propagation: activation spreads along constraint edges,
//! converging toward stability (truth = lowest-energy configuration allowed).

use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct WaveNode {
    pub id: String,
    pub activation: f64,
    pub stability: f64,
}

#[derive(Debug, Clone)]
pub struct WaveEdge {
    pub from: String,
    pub to: String,
    pub weight: f64,
}

#[derive(Debug, Clone, Default)]
pub struct WaveGraph {
    pub nodes: HashMap<String, WaveNode>,
    pub edges: Vec<WaveEdge>,
}

/// One relaxation step: each node pulls toward weighted neighbor mean, damped.
pub fn propagate_wave_step(graph: &mut WaveGraph, damping: f64) {
    let d = damping.clamp(0.0, 1.0);
    let mut next: HashMap<String, f64> = HashMap::new();

    for (id, n) in &graph.nodes {
        let mut sum_w = 0.0;
        let mut sum_v = 0.0;
        for e in &graph.edges {
            if e.from == *id {
                if let Some(nb) = graph.nodes.get(&e.to) {
                    sum_w += e.weight;
                    sum_v += e.weight * nb.activation;
                }
            } else if e.to == *id {
                if let Some(nb) = graph.nodes.get(&e.from) {
                    sum_w += e.weight;
                    sum_v += e.weight * nb.activation;
                }
            }
        }
        let target = if sum_w > 0.0 {
            sum_v / sum_w
        } else {
            n.activation
        };
        let blended = n.activation * (1.0 - d) + target * d;
        next.insert(id.clone(), blended);
    }

    for (id, v) in next {
        if let Some(n) = graph.nodes.get_mut(&id) {
            n.activation = v;
        }
    }
}
