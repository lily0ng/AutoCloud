class ConnectionPooler {
  pool: any[] = [];
  getConnection(): any {
    console.log('🔌 Getting connection from pool');
    return {id: this.pool.length + 1};
  }
}
const pooler = new ConnectionPooler();
pooler.getConnection();
