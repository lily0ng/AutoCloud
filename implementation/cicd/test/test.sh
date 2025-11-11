#!/bin/bash
# Test Script for CI/CD Pipeline

set -e

echo "========================================="
echo "Running Test Suite"
echo "========================================="

# Unit tests
echo "Running unit tests..."
go test ./... -v -cover -coverprofile=coverage.out

# Integration tests
echo "Running integration tests..."
python3 -m pytest tests/ -v --tb=short

# Security scan
echo "Running security scan..."
if command -v gosec &> /dev/null; then
    gosec ./...
fi

# Linting
echo "Running linters..."
if command -v golangci-lint &> /dev/null; then
    golangci-lint run
fi

if command -v pylint &> /dev/null; then
    find . -name "*.py" -exec pylint {} \;
fi

# Code coverage report
echo "Generating coverage report..."
go tool cover -html=coverage.out -o coverage.html

echo "========================================="
echo "All tests passed!"
echo "========================================="
