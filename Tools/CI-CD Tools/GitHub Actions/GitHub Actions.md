# GitHub Actions Guide

GitHub Actions is a powerful automation platform that helps you automate your software development workflows. This guide covers various aspects of GitHub Actions and provides practical examples for different scenarios.

## Table of Contents
- [Basic Concepts](#basic-concepts)
- [Advanced Configurations](#advanced-configurations)
- [Workflow Examples](#workflow-examples)
  - [Python Application](#python-application)
  - [Node.js Application](#nodejs-application)
  - [Docker Container](#docker-container)
  - [Multi-Stage Deployment](#multi-stage-deployment)
  - [Database Migrations](#database-migrations)
  - [Infrastructure as Code](#infrastructure-as-code)
- [Security and Compliance](#security-and-compliance)
- [Advanced Features](#advanced-features)
- [Workflow Optimization](#workflow-optimization)

## Basic Concepts

### Key Components
1. **Workflows**: YAML files that define your automation processes
2. **Events**: Triggers that start your workflow (e.g., push, pull request)
3. **Jobs**: Groups of steps that execute on the same runner
4. **Steps**: Individual tasks within a job
5. **Actions**: Reusable units of code
6. **Runners**: Servers that run your workflows

### Advanced Event Triggers
```yaml
name: Advanced Triggers
on:
  # Push events with path and branch filters
  push:
    branches:
      - main
      - 'releases/**'
    paths:
      - '**.js'
      - '**.jsx'
      - 'package.json'
    tags:
      - 'v*.*.*'
  
  # Pull request events with detailed filters
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main
      - 'releases/**'
    paths-ignore:
      - 'docs/**'
      - '**.md'
  
  # Schedule-based triggers
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
    - cron: '0 12 * * MON'  # Every Monday at noon
  
  # Manual trigger with inputs
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
      debug:
        description: 'Enable debug mode'
        required: false
        type: boolean
```

## Advanced Configurations

### 1. Environment Variables and Secrets
```yaml
name: Environment Config
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    # Global environment variables
    env:
      NODE_ENV: production
      APP_DEBUG: false
      
    steps:
      - uses: actions/checkout@v3
      
      # Using environment variables
      - name: App Configuration
        env:
          API_URL: ${{ secrets.API_URL }}
          DB_CONNECTION: ${{ secrets.DB_CONNECTION }}
          REDIS_URL: ${{ secrets.REDIS_URL }}
          AWS_ACCESS_KEY: ${{ secrets.AWS_ACCESS_KEY }}
          AWS_SECRET_KEY: ${{ secrets.AWS_SECRET_KEY }}
        run: |
          echo "Configuring application..."
          ./scripts/configure.sh
```

### 2. Advanced Job Dependencies and Conditions
```yaml
name: Complex Workflow
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      test_status: ${{ steps.tests.outputs.status }}
    steps:
      - id: tests
        run: |
          echo "::set-output name=status::success"

  security_scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run security scan
        run: |
          echo "Running security scan..."

  build:
    needs: [test, security_scan]
    if: ${{ needs.test.outputs.test_status == 'success' }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - environment: staging
            node-version: 16
          - environment: production
            node-version: 18
    steps:
      - name: Build for ${{ matrix.environment }}
        run: |
          echo "Building for ${{ matrix.environment }}..."
```

### 3. Advanced Docker Configuration
```yaml
name: Docker Advanced Build
on:
  push:
    branches: [ main ]
    tags: [ 'v*.*.*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: user/app
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

### 4. Database Migrations Workflow
```yaml
name: Database Migrations
on:
  push:
    branches: [ main ]
    paths:
      - 'db/migrations/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install alembic psycopg2-binary
      
      - name: Run migrations
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: |
          alembic upgrade head
```

### 5. Infrastructure as Code (Terraform)
```yaml
name: Terraform Deployment
on:
  push:
    branches: [ main ]
    paths:
      - 'terraform/**'

jobs:
  terraform:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.0.0
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Terraform Init
        run: terraform init
        working-directory: ./terraform
      
      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: ./terraform
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve tfplan
        working-directory: ./terraform
```

### 6. Advanced Testing Matrix
```yaml
name: Advanced Testing
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [14.x, 16.x, 18.x]
        include:
          - os: ubuntu-latest
            node-version: 18.x
            experimental: true
            coverage: true
        exclude:
          - os: windows-latest
            node-version: 14.x
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
        
      - name: Upload coverage
        if: ${{ matrix.coverage }}
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

## Security Best Practices

### 1. OIDC Authentication
```yaml
name: OIDC Authentication
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    
    steps:
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions
          aws-region: us-east-1
```

### 2. Environment Protection Rules
```yaml
name: Protected Deployment
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://production.example.com
    permissions:
      deployments: write
      contents: read
    steps:
      - uses: actions/checkout@v3
      
      - name: Create deployment
        uses: chrnorm/deployment-action@v2
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          environment: production
```

## Workflow Optimization Tips

### 1. Caching Strategies
```yaml
name: Optimized Build
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Cache dependencies
      - name: Cache node modules
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-
      
      # Cache build outputs
      - name: Cache build
        uses: actions/cache@v3
        with:
          path: |
            dist
            .next
            build
          key: ${{ runner.os }}-build-${{ github.sha }}
```

### 2. Job Output Handling
```yaml
name: Output Handling
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.build.outputs.image_tag }}
      build_time: ${{ steps.build.outputs.build_time }}
    
    steps:
      - id: build
        run: |
          echo "::set-output name=image_tag::$(date +%s)"
          echo "::set-output name=build_time::$(date)"
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Use build outputs
        run: |
          echo "Deploying image: ${{ needs.build.outputs.image_tag }}"
          echo "Built at: ${{ needs.build.outputs.build_time }}"
```

Remember to:
1. Use specific versions for actions to ensure stability
2. Implement proper error handling and notifications
3. Regularly audit and update workflow permissions
4. Monitor workflow execution times and optimize as needed
5. Implement proper secret management and rotation
6. Use environment protection rules for sensitive deployments