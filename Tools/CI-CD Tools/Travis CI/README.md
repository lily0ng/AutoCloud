# Travis CI Example Project

This is a sample project demonstrating Travis CI integration with a Python Flask application.

## Travis CI Configuration Overview

The `.travis.yml` file contains the following key sections:

1. **Language and Versions**
   - Uses Python 3.8, 3.9, and 3.10
   - Tests across multiple Python versions

2. **Caching**
   - Caches pip packages to speed up builds

3. **Installation Steps**
   - Upgrades pip
   - Installs testing tools (flake8, pytest, coverage)
   - Installs project dependencies

4. **Testing**
   - Runs flake8 for code linting
   - Executes pytest with coverage reporting

5. **Deployment**
   - Configured for Heroku deployment
   - Deploys on successful builds from main branch

## Setup Instructions

1. Fork this repository
2. Sign up for Travis CI (travis-ci.com)
3. Enable Travis CI for your repository
4. Update the `.travis.yml` file:
   - Replace `your-app-name` with your Heroku app name
   - Update the email notification settings
   - Add your encrypted Heroku API key

## Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ --cov=app

# Run application
python app/app.py
```

## CI/CD Pipeline

1. **Push to Repository**
   - Triggers Travis CI build

2. **Build Process**
   - Installs dependencies
   - Runs linting checks
   - Executes tests
   - Generates coverage report

3. **Deployment**
   - Automatically deploys to Heroku on successful builds
