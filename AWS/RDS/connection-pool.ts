// RDS Connection Pool Manager
import { Pool, PoolConfig } from 'pg';

interface ConnectionPoolConfig extends PoolConfig {
  max?: number;
  min?: number;
  idleTimeoutMillis?: number;
  connectionTimeoutMillis?: number;
}

class RDSConnectionPool {
  private pool: Pool;
  private config: ConnectionPoolConfig;

  constructor(config: ConnectionPoolConfig) {
    this.config = {
      max: 20,
      min: 5,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
      ...config
    };

    this.pool = new Pool(this.config);

    this.pool.on('connect', () => {
      console.log('New client connected to the pool');
    });

    this.pool.on('error', (err) => {
      console.error('Unexpected error on idle client', err);
    });
  }

  async query(text: string, params?: any[]): Promise<any> {
    const start = Date.now();
    try {
      const result = await this.pool.query(text, params);
      const duration = Date.now() - start;
      console.log('Executed query', { text, duration, rows: result.rowCount });
      return result;
    } catch (error) {
      console.error('Query error:', error);
      throw error;
    }
  }

  async getClient() {
    return await this.pool.connect();
  }

  async transaction(callback: (client: any) => Promise<any>): Promise<any> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  getPoolStats() {
    return {
      total: this.pool.totalCount,
      idle: this.pool.idleCount,
      waiting: this.pool.waitingCount
    };
  }

  async close(): Promise<void> {
    await this.pool.end();
    console.log('Connection pool closed');
  }
}

// Usage
const poolConfig: ConnectionPoolConfig = {
  host: 'autocloud-db.cluster-xyz.us-east-1.rds.amazonaws.com',
  port: 5432,
  database: 'appdb',
  user: 'admin',
  password: process.env.DB_PASSWORD || 'changeme',
  max: 20,
  min: 5,
  idleTimeoutMillis: 30000
};

const pool = new RDSConnectionPool(poolConfig);

// Example query
pool.query('SELECT * FROM users WHERE id = $1', [1])
  .then(result => console.log(result.rows))
  .catch(err => console.error(err));

// Example transaction
pool.transaction(async (client) => {
  await client.query('INSERT INTO users (name) VALUES ($1)', ['John']);
  await client.query('INSERT INTO logs (action) VALUES ($1)', ['user_created']);
});

export { RDSConnectionPool, ConnectionPoolConfig };
