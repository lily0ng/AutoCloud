class SecretInjector {
  inject(app: string, secrets: Record<string, string>) {
    console.log(`🔐 Injecting ${Object.keys(secrets).length} secrets into ${app}`);
    Object.keys(secrets).forEach(key => {
      console.log(`  ✓ ${key}`);
    });
  }
}
const injector = new SecretInjector();
injector.inject('my-app', {DB_PASSWORD: 'secret', API_KEY: 'key123'});
