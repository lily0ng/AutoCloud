class LogAggregator {
  logs: string[] = [];
  collect(app: string, log: string) {
    this.logs.push(`[${app}] ${log}`);
    console.log(`📝 Log collected from ${app}`);
  }
  query(app: string): string[] {
    return this.logs.filter(l => l.includes(app));
  }
}
const aggregator = new LogAggregator();
aggregator.collect('my-app', 'Application started');
console.log('Logs:', aggregator.query('my-app').length);
