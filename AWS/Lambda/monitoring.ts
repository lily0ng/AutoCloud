// Lambda Monitoring and CloudWatch Integration
import { CloudWatchLogsClient, FilterLogEventsCommand } from '@aws-sdk/client-cloudwatch-logs';
import { CloudWatchClient, GetMetricStatisticsCommand } from '@aws-sdk/client-cloudwatch';

interface MetricQuery {
  functionName: string;
  metricName: string;
  startTime: Date;
  endTime: Date;
  period: number;
}

class LambdaMonitoring {
  private logsClient: CloudWatchLogsClient;
  private metricsClient: CloudWatchClient;

  constructor(region: string = 'us-east-1') {
    this.logsClient = new CloudWatchLogsClient({ region });
    this.metricsClient = new CloudWatchClient({ region });
  }

  async getLogs(functionName: string, startTime: Date, endTime: Date, filterPattern?: string): Promise<any[]> {
    const logGroupName = `/aws/lambda/${functionName}`;

    const command = new FilterLogEventsCommand({
      logGroupName,
      startTime: startTime.getTime(),
      endTime: endTime.getTime(),
      filterPattern
    });

    try {
      const response = await this.logsClient.send(command);
      return response.events || [];
    } catch (error) {
      console.error('Error fetching logs:', error);
      throw error;
    }
  }

  async getMetrics(query: MetricQuery): Promise<any> {
    const command = new GetMetricStatisticsCommand({
      Namespace: 'AWS/Lambda',
      MetricName: query.metricName,
      Dimensions: [
        {
          Name: 'FunctionName',
          Value: query.functionName
        }
      ],
      StartTime: query.startTime,
      EndTime: query.endTime,
      Period: query.period,
      Statistics: ['Average', 'Maximum', 'Minimum', 'Sum']
    });

    try {
      const response = await this.metricsClient.send(command);
      return response.Datapoints;
    } catch (error) {
      console.error('Error fetching metrics:', error);
      throw error;
    }
  }

  async getInvocationMetrics(functionName: string, hours: number = 1): Promise<any> {
    const endTime = new Date();
    const startTime = new Date(endTime.getTime() - hours * 60 * 60 * 1000);

    return await this.getMetrics({
      functionName,
      metricName: 'Invocations',
      startTime,
      endTime,
      period: 300
    });
  }

  async getErrorMetrics(functionName: string, hours: number = 1): Promise<any> {
    const endTime = new Date();
    const startTime = new Date(endTime.getTime() - hours * 60 * 60 * 1000);

    return await this.getMetrics({
      functionName,
      metricName: 'Errors',
      startTime,
      endTime,
      period: 300
    });
  }

  async getDurationMetrics(functionName: string, hours: number = 1): Promise<any> {
    const endTime = new Date();
    const startTime = new Date(endTime.getTime() - hours * 60 * 60 * 1000);

    return await this.getMetrics({
      functionName,
      metricName: 'Duration',
      startTime,
      endTime,
      period: 300
    });
  }

  async getErrorLogs(functionName: string, hours: number = 1): Promise<any[]> {
    const endTime = new Date();
    const startTime = new Date(endTime.getTime() - hours * 60 * 60 * 1000);

    return await this.getLogs(functionName, startTime, endTime, 'ERROR');
  }
}

// Usage
const monitoring = new LambdaMonitoring();

monitoring.getInvocationMetrics('autocloud-function', 24)
  .then(metrics => console.log('Invocation Metrics:', metrics))
  .catch(error => console.error(error));

monitoring.getErrorLogs('autocloud-function', 1)
  .then(logs => console.log('Error Logs:', logs))
  .catch(error => console.error(error));

export { LambdaMonitoring, MetricQuery };
