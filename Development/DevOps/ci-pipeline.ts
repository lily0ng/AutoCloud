import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface PipelineConfig {
  name: string;
  stages: Stage[];
  environment: Record<string, string>;
}

interface Stage {
  name: string;
  steps: Step[];
  condition?: () => boolean;
}

interface Step {
  name: string;
  command: string;
  continueOnError?: boolean;
}

class CIPipeline {
  private config: PipelineConfig;
  private results: Map<string, boolean> = new Map();

  constructor(config: PipelineConfig) {
    this.config = config;
  }

  async run(): Promise<boolean> {
    console.log(`🚀 Starting pipeline: ${this.config.name}`);
    
    for (const stage of this.config.stages) {
      if (stage.condition && !stage.condition()) {
        console.log(`⏭️  Skipping stage: ${stage.name}`);
        continue;
      }

      console.log(`\n📦 Stage: ${stage.name}`);
      const success = await this.runStage(stage);
      
      if (!success) {
        console.log(`❌ Pipeline failed at stage: ${stage.name}`);
        return false;
      }
    }

    console.log('\n✅ Pipeline completed successfully');
    return true;
  }

  private async runStage(stage: Stage): Promise<boolean> {
    for (const step of stage.steps) {
      console.log(`  ▶️  ${step.name}`);
      
      try {
        const { stdout, stderr } = await execAsync(step.command, {
          env: { ...process.env, ...this.config.environment },
        });

        if (stdout) console.log(stdout);
        if (stderr) console.error(stderr);

        this.results.set(step.name, true);
      } catch (error: any) {
        console.error(`  ❌ Failed: ${error.message}`);
        this.results.set(step.name, false);

        if (!step.continueOnError) {
          return false;
        }
      }
    }

    return true;
  }

  getResults(): Map<string, boolean> {
    return this.results;
  }
}

// Example pipeline configuration
const pipelineConfig: PipelineConfig = {
  name: 'Build and Test Pipeline',
  environment: {
    NODE_ENV: 'test',
    CI: 'true',
  },
  stages: [
    {
      name: 'Install Dependencies',
      steps: [
        { name: 'Install npm packages', command: 'npm ci' },
      ],
    },
    {
      name: 'Lint',
      steps: [
        { name: 'Run ESLint', command: 'npm run lint', continueOnError: true },
        { name: 'Run Prettier', command: 'npm run format:check', continueOnError: true },
      ],
    },
    {
      name: 'Type Check',
      steps: [
        { name: 'TypeScript check', command: 'npm run type-check' },
      ],
    },
    {
      name: 'Test',
      steps: [
        { name: 'Run unit tests', command: 'npm run test:unit' },
        { name: 'Run integration tests', command: 'npm run test:integration' },
      ],
    },
    {
      name: 'Build',
      steps: [
        { name: 'Build application', command: 'npm run build' },
      ],
    },
    {
      name: 'Deploy',
      condition: () => process.env.BRANCH === 'main',
      steps: [
        { name: 'Deploy to production', command: 'npm run deploy' },
      ],
    },
  ],
};

// Run pipeline
async function main() {
  const pipeline = new CIPipeline(pipelineConfig);
  const success = await pipeline.run();
  process.exit(success ? 0 : 1);
}

if (require.main === module) {
  main();
}

export { CIPipeline, PipelineConfig, Stage, Step };
