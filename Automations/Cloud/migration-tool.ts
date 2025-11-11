interface MigrationTask {
  id: string;
  source: string;
  destination: string;
  resourceType: string;
  status: 'pending' | 'in-progress' | 'completed' | 'failed';
  progress: number;
}

class MigrationTool {
  private tasks: Map<string, MigrationTask> = new Map();

  createMigrationTask(
    source: string,
    destination: string,
    resourceType: string
  ): MigrationTask {
    const task: MigrationTask = {
      id: `mig-${Date.now()}`,
      source,
      destination,
      resourceType,
      status: 'pending',
      progress: 0,
    };

    this.tasks.set(task.id, task);
    console.log(`📦 Migration task created: ${task.id}`);

    return task;
  }

  async executeMigration(taskId: string): Promise<void> {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    console.log(`🚀 Starting migration: ${task.source} -> ${task.destination}`);
    task.status = 'in-progress';

    // Simulate migration progress
    for (let i = 0; i <= 100; i += 20) {
      task.progress = i;
      console.log(`  Progress: ${i}%`);
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    task.status = 'completed';
    task.progress = 100;
    console.log(`✅ Migration completed: ${taskId}`);
  }

  getTaskStatus(taskId: string): MigrationTask | undefined {
    return this.tasks.get(taskId);
  }

  listTasks(): MigrationTask[] {
    return Array.from(this.tasks.values());
  }

  async migrateMultipleResources(migrations: Array<{
    source: string;
    destination: string;
    resourceType: string;
  }>): Promise<void> {
    console.log(`🔄 Starting batch migration of ${migrations.length} resources...`);

    const tasks = migrations.map(m =>
      this.createMigrationTask(m.source, m.destination, m.resourceType)
    );

    for (const task of tasks) {
      await this.executeMigration(task.id);
    }

    console.log('✅ Batch migration completed');
  }

  generateMigrationReport(): void {
    console.log('\n📋 Migration Report');
    console.log('===================');

    const tasks = this.listTasks();
    const completed = tasks.filter(t => t.status === 'completed').length;
    const failed = tasks.filter(t => t.status === 'failed').length;
    const inProgress = tasks.filter(t => t.status === 'in-progress').length;

    console.log(`Total Tasks: ${tasks.length}`);
    console.log(`Completed: ${completed}`);
    console.log(`Failed: ${failed}`);
    console.log(`In Progress: ${inProgress}`);

    console.log('\nTask Details:');
    tasks.forEach(task => {
      const statusIcon = {
        pending: '⏳',
        'in-progress': '🔄',
        completed: '✅',
        failed: '❌',
      }[task.status];

      console.log(`${statusIcon} ${task.id}: ${task.source} -> ${task.destination} (${task.progress}%)`);
    });
  }
}

// Example usage
const migrationTool = new MigrationTool();

migrationTool.migrateMultipleResources([
  { source: 'aws:us-east-1:vm-1', destination: 'gcp:us-central1:vm-1', resourceType: 'VM' },
  { source: 'aws:us-east-1:db-1', destination: 'azure:eastus:db-1', resourceType: 'Database' },
]).then(() => {
  migrationTool.generateMigrationReport();
});
