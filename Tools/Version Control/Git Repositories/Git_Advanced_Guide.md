# Advanced Git Operations Guide

## 1. Git Workflows

### GitFlow Workflow
```bash
# Initialize GitFlow
git flow init

# Feature development
git flow feature start new-feature
git flow feature finish new-feature

# Release management
git flow release start v1.0.0
git flow release finish v1.0.0

# Hotfix handling
git flow hotfix start bug-fix
git flow hotfix finish bug-fix
```

### Trunk-Based Development
```bash
# Create short-lived feature branch
git checkout -b feature/quick-fix
# Make changes, commit, and merge quickly back to main
git checkout main
git merge feature/quick-fix
```

## 2. Advanced Git Commands

### Interactive Rebase
```bash
# Rebase last N commits
git rebase -i HEAD~3

# Common rebase commands:
# p, pick = use commit
# r, reword = use commit but edit message
# e, edit = use commit but stop for amending
# s, squash = use commit but meld into previous commit
# f, fixup = like squash, but discard commit message
# d, drop = remove commit
```

### Reflog Operations
```bash
# View reflog
git reflog

# Recover deleted branch
git checkout -b recovered-branch HEAD@{1}

# Restore to specific reflog entry
git reset --hard HEAD@{2}
```

### Submodules
```bash
# Add submodule
git submodule add https://github.com/user/repo path/to/submodule

# Initialize submodules
git submodule init
git submodule update

# Update all submodules
git submodule update --remote --merge
```

## 3. Git Hooks

### Pre-commit Hook Example
```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run tests before commit
npm test

# Check code style
eslint .

# Exit with non-zero status if any checks fail
```

### Pre-push Hook Example
```bash
#!/bin/sh
# .git/hooks/pre-push

# Run integration tests
npm run test:integration

# Check for sensitive data
grep -r "API_KEY" .
```

## 4. Advanced Merging Strategies

### Merge Strategies
```bash
# Recursive strategy with ours
git merge -X ours feature-branch

# Recursive strategy with theirs
git merge -X theirs feature-branch

# Octopus merge (multiple branches)
git merge branch1 branch2 branch3
```

### Resolving Complex Conflicts
```bash
# Use merge tool
git mergetool

# Abort merge
git merge --abort

# Continue merge after resolving
git merge --continue
```

## 5. Git Internals

### Object Database
```bash
# View object content
git cat-file -p <hash>

# List all objects
git rev-list --objects --all

# Garbage collection
git gc
```

### Pack Files
```bash
# Create pack file
git gc --prune=now

# List pack contents
git verify-pack -v .git/objects/pack/pack-*.idx
```

## 6. Repository Maintenance

### Cleaning and Optimization
```bash
# Remove untracked files and directories
git clean -fd

# Compress repository
git gc --aggressive

# Remove old reflog entries
git reflog expire --expire=90.days.ago --all
```

### Large File Management
```bash
# Find large files
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | sed -n 's/^blob //p' \
  | sort -k2nr \
  | head -10

# Remove large files from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/large/file' \
  --prune-empty --tag-name-filter cat -- --all
```

## 7. Advanced Branching

### Branch Management
```bash
# List merged branches
git branch --merged

# List unmerged branches
git branch --no-merged

# Delete merged branches
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d
```

### Branch Protection
```bash
# Create protected branch
git branch -M protected-branch
git push -u origin protected-branch

# Configure branch protection (GitHub API)
curl -X PUT -H "Authorization: token YOUR-TOKEN" \
     -d '{"required_status_checks": {"strict": true}}' \
     https://api.github.com/repos/owner/repo/branches/main/protection
```

## 8. Git Security

### Signing Commits
```bash
# Configure GPG key
git config --global user.signingkey YOUR-GPG-KEY-ID

# Sign commits
git commit -S -m "Signed commit message"

# Sign tags
git tag -s v1.0.0 -m "Signed tag"
```

### Credential Management
```bash
# Configure credential helper
git config --global credential.helper store

# Clear stored credentials
git credential-cache exit
```

## 9. Automation and CI/CD

### Git Aliases
```bash
# Add useful aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.unstage 'reset HEAD --'
```

### GitHub Actions Example
```yaml
name: Git Automation
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: |
        npm install
        npm test
```

Remember to:
- Always backup before major operations
- Test complex commands in a safe environment first
- Keep security in mind when handling sensitive data
- Document your Git workflows for team collaboration
