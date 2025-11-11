# Branch Management Commands

## Basic Branch Operations

### Creating Branches
```bash
# Create a new branch
git branch <branch-name>

# Create and switch to new branch
git checkout -b <branch-name>

# Create branch from specific commit
git branch <branch-name> <commit-hash>

# Create branch from tag
git branch <branch-name> <tag-name>
```

### Listing Branches
```bash
# List local branches
git branch

# List remote branches
git branch -r

# List all branches (local and remote)
git branch -a

# Show last commit on each branch
git branch -v

# Show merged branches
git branch --merged

# Show unmerged branches
git branch --no-merged
```

### Switching Branches
```bash
# Switch to existing branch
git checkout <branch-name>

# Switch to previous branch
git checkout -

# Switch to remote branch
git checkout -b <branch-name> origin/<branch-name>
```

## Advanced Branch Operations

### Merging
```bash
# Merge branch into current branch
git merge <branch-name>

# Merge with no fast-forward
git merge --no-ff <branch-name>

# Abort merge in case of conflicts
git merge --abort
```

### Rebasing
```bash
# Rebase current branch onto another
git rebase <branch-name>

# Interactive rebase
git rebase -i <branch-name>

# Abort rebase
git rebase --abort

# Continue rebase after resolving conflicts
git rebase --continue
```

### Branch Management
```bash
# Rename branch
git branch -m <old-name> <new-name>

# Delete local branch
git branch -d <branch-name>

# Force delete local branch
git branch -D <branch-name>

# Delete remote branch
git push origin --delete <branch-name>
```

### Remote Operations
```bash
# Push branch to remote
git push origin <branch-name>

# Push and set upstream
git push -u origin <branch-name>

# Fetch remote branches
git fetch origin

# Prune deleted remote branches
git remote prune origin

# Update local branch list
git fetch --prune
```

## Branch Comparison

### Viewing Differences
```bash
# Compare branches
git diff <branch1>..<branch2>

# Show file differences between branches
git diff <branch1>..<branch2> -- <file-path>

# Show branch divergence point
git merge-base <branch1> <branch2>
```

### Branch Information
```bash
# Show branch history
git log <branch-name>

# Show branch topology
git log --graph --oneline --all

# Show commit history between branches
git log <branch1>..<branch2>

# Show who modified which lines
git blame <file-name>
```

## Cherry-picking
```bash
# Cherry-pick a commit
git cherry-pick <commit-hash>

# Cherry-pick without committing
git cherry-pick -n <commit-hash>

# Cherry-pick a range of commits
git cherry-pick <start-commit>..<end-commit>
```

## Stashing
```bash
# Stash changes
git stash

# List stashes
git stash list

# Apply stash
git stash apply

# Pop stash
git stash pop

# Drop stash
git stash drop
```

## Recovery Operations
```bash
# Recover deleted branch
git reflog
git checkout -b <branch-name> <commit-hash>

# Reset to specific commit
git reset --hard <commit-hash>

# Undo last commit keeping changes
git reset --soft HEAD~1
```
