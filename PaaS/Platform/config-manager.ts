class ConfigManager {
  configs: Map<string, any> = new Map();
  set(key: string, value: any) {
    this.configs.set(key, value);
    console.log(`⚙️  Config set: ${key}`);
  }
  get(key: string): any {
    return this.configs.get(key);
  }
}
const config = new ConfigManager();
config.set('DATABASE_URL', 'postgres://localhost/db');
console.log('Config:', config.get('DATABASE_URL'));
