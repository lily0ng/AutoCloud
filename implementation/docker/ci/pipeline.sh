#!/bin/bash
# CI/CD Pipeline Script

set -e

STAGE=${1:-all}

run_build() {
    echo "========================================="
    echo "Stage: Build"
    echo "========================================="
    ./docker/scripts/build-all.sh
}

run_test() {
    echo "========================================="
    echo "Stage: Test"
    echo "========================================="
    docker-compose -f docker/docker-compose.test.yml up --abort-on-container-exit
}

run_scan() {
    echo "========================================="
    echo "Stage: Security Scan"
    echo "========================================="
    docker build -t security-scanner -f docker/security/Dockerfile.security-scanner .
    docker run --rm security-scanner
}

run_push() {
    echo "========================================="
    echo "Stage: Push"
    echo "========================================="
    ./docker/scripts/push-all.sh
}

run_deploy() {
    echo "========================================="
    echo "Stage: Deploy"
    echo "========================================="
    kubectl apply -f infrastructure/kubernetes/
}

case $STAGE in
    build)
        run_build
        ;;
    test)
        run_test
        ;;
    scan)
        run_scan
        ;;
    push)
        run_push
        ;;
    deploy)
        run_deploy
        ;;
    all)
        run_build
        run_test
        run_scan
        run_push
        run_deploy
        ;;
    *)
        echo "Usage: $0 {build|test|scan|push|deploy|all}"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "Pipeline stage '$STAGE' completed!"
echo "========================================="
