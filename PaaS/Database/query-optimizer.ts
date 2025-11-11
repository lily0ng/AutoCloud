class QueryOptimizer {
  optimize(query: string): string {
    console.log(`⚡ Optimizing query: ${query.substring(0, 50)}...`);
    return query + ' USE INDEX(idx_user_id)';
  }
}
const optimizer = new QueryOptimizer();
optimizer.optimize('SELECT * FROM users WHERE id = 1');
