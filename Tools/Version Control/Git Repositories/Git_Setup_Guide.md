# Git Repository Setup and Configuration Guide

## 1. Initial Git Configuration

### Basic Configuration
```bash
# Set your username
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"

# Set default branch name (optional)
git config --global init.defaultBranch main

# Configure default editor
git config --global core.editor "vim"  # or your preferred editor
```

### View Current Configuration
```bash
# View all configurations
git config --list

# View specific configuration
git config user.name
git config user.email
```

## 2. Creating a New Git Repository

### Local Repository Setup
```bash
# Create a new directory
mkdir project-name
cd project-name

# Initialize git repository
git init

# Verify initialization
ls -la  # Look for .git directory
```

### Basic Repository Structure
```bash
# Create basic project files
touch README.md
touch .gitignore
```

Example `.gitignore` content:
```
# OS files
.DS_Store
Thumbs.db

# IDE files
.idea/
.vscode/

# Dependencies
node_modules/
venv/
__pycache__/

# Build files
dist/
build/
*.log
```

## 3. Working with Git Repository

### Basic Git Commands
```bash
# Check repository status
git status

# Add files to staging
git add <filename>      # Add specific file
git add .              # Add all files

# Commit changes
git commit -m "Initial commit"

# View commit history
git log
git log --oneline      # Compact view
```

### Branching
```bash
# Create and switch to new branch
git checkout -b feature-branch

# List all branches
git branch

# Switch branches
git checkout main

# Merge branches
git merge feature-branch
```

## 4. Remote Repository Setup

### Connecting to Remote
```bash
# Add remote repository
git remote add origin <remote-repository-url>

# Verify remote
git remote -v

# Push to remote
git push -u origin main
```

### Common Remote Operations
```bash
# Fetch updates
git fetch origin

# Pull updates
git pull origin main

# Push changes
git push origin main
```

## 5. Best Practices

1. **Commit Messages**
   - Write clear, descriptive commit messages
   - Use present tense ("Add feature" not "Added feature")
   - Keep first line under 50 characters
   - Add detailed description if needed after blank line

2. **Branching Strategy**
   - main/master: stable production code
   - develop: integration branch
   - feature/*: new features
   - hotfix/*: urgent fixes
   - release/*: release preparation

3. **Regular Operations**
   - Commit frequently
   - Pull before pushing
   - Review changes before committing
   - Keep commits atomic and focused

## 6. Useful Git Commands

### Repository Maintenance
```bash
# Clean untracked files
git clean -n  # dry run
git clean -f  # force clean

# Stash changes
git stash
git stash pop

# Amend last commit
git commit --amend

# Reset changes
git reset --hard HEAD  # Reset to last commit
git reset --soft HEAD~1  # Undo last commit keeping changes
```

### Advanced Operations
```bash
# Rebase
git rebase main

# Cherry-pick
git cherry-pick <commit-hash>

# Tag versions
git tag -a v1.0.0 -m "Version 1.0.0"
```

## 7. Troubleshooting

Common issues and solutions:
1. **Merge Conflicts**
   ```bash
   # Resolve conflicts manually
   git status  # Check conflicting files
   # Edit files to resolve conflicts
   git add <resolved-files>
   git commit -m "Resolve merge conflicts"
   ```

2. **Undo Operations**
   ```bash
   # Undo last commit
   git reset --soft HEAD~1

   # Discard local changes
   git checkout -- <file>
   ```

Remember to always backup important data before performing major Git operations!
