class FlowLogs {
  enable(resourceId: string, destination: string) {
    console.log(`📊 Flow logs enabled for ${resourceId} -> ${destination}`);
  }
}
const logs = new FlowLogs();
logs.enable('vpc-123', 's3://flow-logs-bucket');
