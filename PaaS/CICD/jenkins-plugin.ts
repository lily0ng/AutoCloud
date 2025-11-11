class JenkinsPlugin {
  buildJob(job: string, params: Record<string, string>) {
    console.log(`🔨 Building Jenkins job: ${job}`);
    console.log('  Params:', params);
  }
}
const jenkins = new JenkinsPlugin();
jenkins.buildJob('build-app', {branch: 'main', env: 'prod'});
