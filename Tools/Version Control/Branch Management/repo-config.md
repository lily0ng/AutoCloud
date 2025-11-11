# Repository Configuration Guide

## Repository-Specific Configuration

### Branch Protection Rules
```bash
# Create a .gitconfig file in your repository
[branch "main"]
    # Require pull request reviews before merging
    mergeable = true
    # Require status checks to pass before merging
    protection = true
    # Require branches to be up to date before merging
    requireUpToDate = true
```

### Git Attributes
Create a `.gitattributes` file:
```bash
# Auto detect text files and perform LF normalization
* text=auto

# Specific file types
*.txt text
*.md text
*.js text
*.py text
*.java text

# Binary files
*.png binary
*.jpg binary
*.pdf binary
```

### Git Hooks
Common hooks for branch management (place in `.git/hooks/`):

#### pre-commit
```bash
#!/bin/sh
# Prevent commits directly to main branch
branch="$(git rev-parse --abbrev-ref HEAD)"
if [ "$branch" = "main" ]; then
    echo "Cannot commit directly to main branch"
    exit 1
fi
```

#### pre-push
```bash
#!/bin/sh
# Run tests before pushing
npm test  # or your test command
```

### Repository-Specific Branch Settings
```bash
# Configure branch specific merge settings
git config branch.feature/*.mergeoptions "--no-ff"

# Set up branch specific remote
git config branch.feature/*.remote origin
git config branch.feature/*.merge refs/heads/feature/
```

## Branch Naming Conventions
```plaintext
feature/   # New features
bugfix/    # Bug fixes
hotfix/    # Urgent fixes for production
release/   # Release preparation
docs/      # Documentation updates
test/      # Test development
```

## Commit Message Template
Create a `.gitmessage` file:
```plaintext
# <type>: <subject>
# |<----  Using a Maximum Of 50 Characters  ---->|

# Explain why this change is being made
# |<----   Try To Limit Each Line to a Maximum Of 72 Characters   ---->|

# --- COMMIT END ---
# Type can be
#    feat     (new feature)
#    fix      (bug fix)
#    refactor (refactoring code)
#    style    (formatting, missing semicolons, etc; no code change)
#    docs     (changes to documentation)
#    test     (adding or refactoring tests; no production code change)
#    chore    (updating grunt tasks etc; no production code change)
# --------------------
# Remember to
#   - Capitalize the subject line
#   - Use the imperative mood in the subject line
#   - Do not end the subject line with a period
#   - Separate subject from body with a blank line
#   - Use the body to explain what and why vs. how
#   - Can use multiple lines with "-" for bullet points in body
# --------------------
```

Configure git to use the commit template:
```bash
git config commit.template .gitmessage
```
