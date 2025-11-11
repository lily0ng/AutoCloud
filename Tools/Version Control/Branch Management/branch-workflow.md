# Git Branch Workflow Strategies

## 1. GitFlow Workflow
```plaintext
main
  └── develop
       ├── feature/feature1
       ├── feature/feature2
       ├── release/1.0.0
       └── hotfix/critical-fix
```

### Implementation
```bash
# Initialize GitFlow
git flow init

# Start a feature
git flow feature start feature_name
git flow feature finish feature_name

# Start a release
git flow release start 1.0.0
git flow release finish '1.0.0'

# Create a hotfix
git flow hotfix start critical-fix
git flow hotfix finish critical-fix
```

## 2. Trunk-Based Development
```plaintext
main
  ├── feature-flag/new-ui
  └── short-lived/quick-fix
```

### Implementation
```bash
# Create short-lived feature branch
git checkout -b feature/quick-win
# Merge frequently (at least daily)
git checkout main
git merge feature/quick-win
```

## 3. Environment-Based Branching
```plaintext
main
  ├── staging
  ├── qa
  └── development
```

### Implementation
```bash
# Create environment branches
git checkout -b development
git checkout -b staging
git checkout -b qa

# Promote changes through environments
git checkout staging
git merge development
git checkout qa
git merge staging
```

## 4. Release Train Model
```plaintext
main
  ├── release/2024.1
  ├── release/2024.2
  └── release/2024.3
```

### Implementation
```bash
# Create release branch
git checkout -b release/2024.1
# Cherry-pick features
git cherry-pick <commit-hash>
# Stabilize and merge
git checkout main
git merge release/2024.1
```

## 5. Feature Toggles Workflow
```bash
# Install feature toggle library
npm install feature-toggle

# Implementation example
if (featureToggle.isEnabled('new-feature')) {
    // new implementation
} else {
    // old implementation
}
```
