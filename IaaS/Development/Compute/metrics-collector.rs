use std::collections::HashMap;

pub struct MetricsCollector {
    metrics: HashMap<String, f64>,
}

impl MetricsCollector {
    pub fn new() -> Self {
        MetricsCollector {
            metrics: HashMap::new(),
        }
    }
    
    pub fn record(&mut self, name: &str, value: f64) {
        self.metrics.insert(name.to_string(), value);
        println!("📊 Metric recorded: {} = {}", name, value);
    }
    
    pub fn get(&self, name: &str) -> Option<&f64> {
        self.metrics.get(name)
    }
}

fn main() {
    let mut collector = MetricsCollector::new();
    collector.record("cpu_usage", 75.5);
    collector.record("memory_usage", 60.2);
    println!("✅ Metrics collected");
}
