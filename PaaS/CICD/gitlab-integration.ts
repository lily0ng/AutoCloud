class GitLabIntegration {
  triggerPipeline(project: string, ref: string) {
    console.log(`🔄 Triggering pipeline for ${project} on ${ref}`);
  }
}
const gitlab = new GitLabIntegration();
gitlab.triggerPipeline('mygroup/myproject', 'main');
