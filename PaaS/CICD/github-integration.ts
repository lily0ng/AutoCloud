class GitHubIntegration {
  triggerWorkflow(repo: string, workflow: string) {
    console.log(`🔄 Triggering ${workflow} on ${repo}`);
  }
}
const github = new GitHubIntegration();
github.triggerWorkflow('myorg/myrepo', 'ci.yml');
