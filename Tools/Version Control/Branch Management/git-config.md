# Git Configuration Guide

## Global Git Configuration

### Basic Configuration
```bash
# Set user information
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Set default editor
git config --global core.editor "vim"
```

### Branch Configuration
```bash
# Enable auto-setup of remote tracking
git config --global branch.autoSetupMerge always

# Configure pull behavior
git config --global pull.rebase false  # merge (the default strategy)
# or
git config --global pull.rebase true   # rebase
# or
git config --global pull.ff only       # fast-forward only
```

### Merge and Diff Configuration
```bash
# Set merge tool
git config --global merge.tool vimdiff

# Enable colored output
git config --global color.ui auto

# Configure diff tool
git config --global diff.tool vimdiff
```

### Alias Configuration
```bash
# Useful aliases for branch management
git config --global alias.br "branch"
git config --global alias.co "checkout"
git config --global alias.cb "checkout -b"
git config --global alias.st "status"
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
```

## Viewing Configuration
```bash
# View all configurations
git config --list

# View specific configuration
git config user.name
git config user.email
```

## Configuration File Locations
- System-wide: `/etc/gitconfig`
- Global (user): `~/.gitconfig`
- Repository: `.git/config`
