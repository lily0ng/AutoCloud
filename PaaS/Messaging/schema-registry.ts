class SchemaRegistry {
  schemas: Map<string, any> = new Map();
  register(topic: string, schema: any) {
    this.schemas.set(topic, schema);
    console.log(`📋 Schema registered for ${topic}`);
  }
}
const registry = new SchemaRegistry();
registry.register('events', {type: 'object', properties: {id: 'string'}});
