// RDS Database Migration Tool
import { RDSClient, DescribeDBInstancesCommand } from '@aws-sdk/client-rds';
import { DatabaseMigrationServiceClient, CreateReplicationTaskCommand } from '@aws-sdk/client-database-migration-service';

interface MigrationConfig {
  sourceEndpoint: string;
  targetEndpoint: string;
  replicationInstance: string;
  tableMappings: string;
  migrationType: 'full-load' | 'cdc' | 'full-load-and-cdc';
}

class DatabaseMigrationTool {
  private rdsClient: RDSClient;
  private dmsClient: DatabaseMigrationServiceClient;

  constructor(region: string = 'us-east-1') {
    this.rdsClient = new RDSClient({ region });
    this.dmsClient = new DatabaseMigrationServiceClient({ region });
  }

  async createMigrationTask(config: MigrationConfig): Promise<string> {
    const command = new CreateReplicationTaskCommand({
      ReplicationTaskIdentifier: `migration-${Date.now()}`,
      SourceEndpointArn: config.sourceEndpoint,
      TargetEndpointArn: config.targetEndpoint,
      ReplicationInstanceArn: config.replicationInstance,
      MigrationType: config.migrationType,
      TableMappings: config.tableMappings,
      ReplicationTaskSettings: JSON.stringify({
        TargetMetadata: {
          SupportLobs: true,
          FullLobMode: false,
          LobChunkSize: 64,
          LimitedSizeLobMode: true,
          LobMaxSize: 32
        },
        FullLoadSettings: {
          TargetTablePrepMode: 'DROP_AND_CREATE',
          CreatePkAfterFullLoad: false,
          StopTaskCachedChangesApplied: false,
          StopTaskCachedChangesNotApplied: false,
          MaxFullLoadSubTasks: 8
        },
        Logging: {
          EnableLogging: true
        }
      })
    });

    try {
      const response = await this.dmsClient.send(command);
      const taskArn = response.ReplicationTask?.ReplicationTaskArn || '';
      console.log(`Migration task created: ${taskArn}`);
      return taskArn;
    } catch (error) {
      console.error('Error creating migration task:', error);
      throw error;
    }
  }

  async getDBInstanceInfo(dbInstanceId: string): Promise<any> {
    const command = new DescribeDBInstancesCommand({
      DBInstanceIdentifier: dbInstanceId
    });

    try {
      const response = await this.rdsClient.send(command);
      return response.DBInstances?.[0];
    } catch (error) {
      console.error('Error getting DB instance info:', error);
      throw error;
    }
  }

  generateTableMappings(schemas: string[], tables: string[]): string {
    return JSON.stringify({
      rules: [
        {
          'rule-type': 'selection',
          'rule-id': '1',
          'rule-name': '1',
          'object-locator': {
            'schema-name': schemas.join('|'),
            'table-name': tables.join('|')
          },
          'rule-action': 'include'
        }
      ]
    });
  }
}

// Usage
const migrationTool = new DatabaseMigrationTool();

const config: MigrationConfig = {
  sourceEndpoint: 'arn:aws:dms:us-east-1:123456789:endpoint:SOURCE',
  targetEndpoint: 'arn:aws:dms:us-east-1:123456789:endpoint:TARGET',
  replicationInstance: 'arn:aws:dms:us-east-1:123456789:rep:INSTANCE',
  tableMappings: migrationTool.generateTableMappings(['public'], ['%']),
  migrationType: 'full-load-and-cdc'
};

migrationTool.createMigrationTask(config);

export { DatabaseMigrationTool, MigrationConfig };
