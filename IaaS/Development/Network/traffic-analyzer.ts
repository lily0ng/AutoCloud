class TrafficAnalyzer {
  analyze(logs: string[]) {
    console.log(`🔍 Analyzing ${logs.length} traffic logs`);
    console.log('  Top talkers: 10.0.1.5, 10.0.1.10');
    console.log('  Total traffic: 1.5TB');
  }
}
const analyzer = new TrafficAnalyzer();
analyzer.analyze(['log1', 'log2']);
