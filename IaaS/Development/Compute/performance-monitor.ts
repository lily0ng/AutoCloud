interface PerformanceMetrics {
  cpu: number;
  memory: number;
  disk: number;
  network: number;
}

class PerformanceMonitor {
  monitor(): PerformanceMetrics {
    const metrics = {
      cpu: Math.random() * 100,
      memory: Math.random() * 100,
      disk: Math.random() * 100,
      network: Math.random() * 1000,
    };
    console.log(`📊 Performance: CPU ${metrics.cpu.toFixed(1)}%, MEM ${metrics.memory.toFixed(1)}%`);
    return metrics;
  }
}

const monitor = new PerformanceMonitor();
monitor.monitor();
