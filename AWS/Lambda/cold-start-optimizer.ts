// Lambda Cold Start Optimizer
import { LambdaClient, InvokeCommand, UpdateFunctionConfigurationCommand } from '@aws-sdk/client-lambda';

interface OptimizationConfig {
  functionName: string;
  memorySize?: number;
  provisionedConcurrency?: number;
  warmupSchedule?: string;
}

class ColdStartOptimizer {
  private client: LambdaClient;

  constructor(region: string = 'us-east-1') {
    this.client = new LambdaClient({ region });
  }

  async optimizeMemory(functionName: string, targetMemory: number): Promise<void> {
    const command = new UpdateFunctionConfigurationCommand({
      FunctionName: functionName,
      MemorySize: targetMemory
    });

    try {
      await this.client.send(command);
      console.log(`Updated memory size to ${targetMemory}MB`);
    } catch (error) {
      console.error('Error updating memory:', error);
      throw error;
    }
  }

  async warmupFunction(functionName: string): Promise<void> {
    const command = new InvokeCommand({
      FunctionName: functionName,
      InvocationType: 'Event',
      Payload: Buffer.from(JSON.stringify({ warmup: true }))
    });

    try {
      await this.client.send(command);
      console.log(`Warmup invocation sent to ${functionName}`);
    } catch (error) {
      console.error('Error warming up function:', error);
      throw error;
    }
  }

  async scheduleWarmup(functionName: string, intervalMinutes: number): Promise<NodeJS.Timeout> {
    console.log(`Scheduling warmup every ${intervalMinutes} minutes`);
    
    return setInterval(async () => {
      try {
        await this.warmupFunction(functionName);
      } catch (error) {
        console.error('Warmup failed:', error);
      }
    }, intervalMinutes * 60 * 1000);
  }

  async measureColdStart(functionName: string, iterations: number = 10): Promise<number[]> {
    const coldStartTimes: number[] = [];

    for (let i = 0; i < iterations; i++) {
      const startTime = Date.now();
      
      const command = new InvokeCommand({
        FunctionName: functionName,
        InvocationType: 'RequestResponse',
        Payload: Buffer.from(JSON.stringify({ test: true }))
      });

      try {
        await this.client.send(command);
        const duration = Date.now() - startTime;
        coldStartTimes.push(duration);
        console.log(`Iteration ${i + 1}: ${duration}ms`);
        
        // Wait before next iteration to ensure cold start
        await new Promise(resolve => setTimeout(resolve, 60000));
      } catch (error) {
        console.error(`Error in iteration ${i + 1}:`, error);
      }
    }

    return coldStartTimes;
  }

  calculateAverageColdStart(times: number[]): number {
    return times.reduce((a, b) => a + b, 0) / times.length;
  }

  async optimizeConfiguration(config: OptimizationConfig): Promise<void> {
    console.log(`Optimizing configuration for ${config.functionName}`);

    if (config.memorySize) {
      await this.optimizeMemory(config.functionName, config.memorySize);
    }

    if (config.warmupSchedule) {
      const intervalMinutes = parseInt(config.warmupSchedule);
      await this.scheduleWarmup(config.functionName, intervalMinutes);
    }

    console.log('Optimization completed');
  }
}

// Usage
const optimizer = new ColdStartOptimizer();

// Measure cold start times
optimizer.measureColdStart('autocloud-function', 5)
  .then(times => {
    const avg = optimizer.calculateAverageColdStart(times);
    console.log(`Average cold start: ${avg}ms`);
  });

// Optimize configuration
optimizer.optimizeConfiguration({
  functionName: 'autocloud-function',
  memorySize: 1024,
  warmupSchedule: '5'
});

export { ColdStartOptimizer, OptimizationConfig };
