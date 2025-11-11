#!/bin/bash
# Code Quality Checks
set -e

echo "📊 Running code quality checks..."

# Linting
npm run lint

# Type checking
npm run type-check

# Code coverage
npm run test:coverage

# Complexity analysis
if command -v complexity-report &> /dev/null; then
    complexity-report src/
fi

echo "✅ Code quality checks complete"
