# Pull Request Guide

## Table of Contents
1. [Creating a Pull Request](#creating-a-pull-request)
2. [Pull Request Best Practices](#pull-request-best-practices)
3. [Pull Request Template](#pull-request-template)
4. [Review Process](#review-process)

## Creating a Pull Request

### Step 1: Prepare Your Branch
1. Ensure your local repository is up to date:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Create a new feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Step 2: Make Your Changes
1. Make your code changes
2. Commit your changes with meaningful messages:
   ```bash
   git add .
   git commit -m "descriptive commit message"
   ```
3. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

### Step 3: Create the Pull Request
1. Go to your repository on GitHub/GitLab
2. Click "New Pull Request"
3. Select your feature branch as the compare branch
4. Fill in the PR template

## Pull Request Best Practices

### Naming Convention
- Use a clear, descriptive title
- Follow the format: `[Type] Brief description`
- Types: Feature, Fix, Docs, Style, Refactor, Test, Chore

### Size and Scope
- Keep PRs small and focused
- One PR should address one concern
- Aim for less than 400 lines of code changes
- Break large changes into smaller PRs

### Documentation
- Include relevant documentation updates
- Add comments for complex logic
- Update README if necessary

## Pull Request Template

```markdown
## Description
[Provide a brief description of the changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
[Describe the tests you ran]

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
```

## Review Process

### For Authors
1. **Self-Review**
   - Review your own code first
   - Check for style consistency
   - Ensure tests pass
   - Verify documentation is updated

2. **Respond to Reviews**
   - Address all comments
   - Be open to feedback
   - Make requested changes promptly

### For Reviewers
1. **Code Review Guidelines**
   - Check code quality and style
   - Verify test coverage
   - Review documentation
   - Test functionality if possible

2. **Providing Feedback**
   - Be constructive and specific
   - Explain the reasoning behind suggestions
   - Use a collaborative tone

### Merging Criteria
- All required reviews completed
- CI/CD pipelines passing
- No merge conflicts
- All discussions resolved
- Documentation updated
