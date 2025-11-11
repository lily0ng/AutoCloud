# Git Branch Troubleshooting Guide

## 1. Common Branch Issues

### Detached HEAD State
```bash
# Check current state
git status

# Recovery options
# Option 1: Create new branch
git branch new-branch-name

# Option 2: Attach to existing branch
git checkout existing-branch
```

### Lost Commits
```bash
# Find lost commits
git reflog

# Recover commit
git cherry-pick <commit-hash>

# Recover branch
git checkout -b recovery-branch <commit-hash>
```

### Merge Conflicts
```bash
# Abort merge
git merge --abort

# Use visual tool
git mergetool

# Reset to pre-merge state
git reset --hard HEAD
```

## 2. Remote Repository Issues

### Push Rejection
```bash
# Force push (use with caution!)
git push --force-with-lease origin branch-name

# Update local branch
git fetch origin
git rebase origin/branch-name

# Check remote status
git remote show origin
```

### Branch Synchronization
```bash
# Reset to match remote
git fetch origin
git reset --hard origin/branch-name

# Clean up remote tracking
git remote prune origin
git fetch --prune
```

## 3. Performance Issues

### Slow Operations
```bash
# Optimize repository
git gc
git prune

# Create shallow clone
git clone --depth 1 <repository-url>

# Use partial clone
git clone --filter=blob:none <repository-url>
```

### Large Repository
```bash
# Analyze repository size
git count-objects -vH

# Find large files
git rev-list --objects --all |
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  sed -n 's/^blob //p' |
  sort -rn -k2 |
  head -10

# Use Git LFS
git lfs migrate import --include="*.psd,*.zip"
```

## 4. Access and Permission Issues

### Authentication Problems
```bash
# Update credentials
git config --global credential.helper store

# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Test SSH connection
ssh -T git@github.com
```

### Branch Protection
```bash
# Check branch protection
git push origin branch-name

# Request access
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"
```

## 5. Data Recovery

### Recover Deleted Branch
```bash
# Find last commit
git reflog
git checkout -b branch-name <commit-hash>

# Recover from backup refs
git fsck --full
git checkout -b recovered-branch <dangling-commit>
```

### Undo Mistakes
```bash
# Undo last commit
git reset --soft HEAD~1

# Undo merge
git reset --hard ORIG_HEAD

# Revert changes
git revert <commit-hash>
```

## 6. Advanced Troubleshooting

### Debugging Tools
```bash
# Debug with bisect
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>

# Trace file history
git log --follow -p -- file.txt

# Check blame information
git blame -C -L 10,20 file.txt
```

### Repository Repair
```bash
# Check repository health
git fsck --full

# Repair corrupted objects
git prune
git repack -a -d

# Verify connectivity
git gc --aggressive --prune=now
```
