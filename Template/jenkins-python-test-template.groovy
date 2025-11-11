pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = "3.11"
        VIRTUAL_ENV = "${WORKSPACE}/venv"
    }
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to test')
        booleanParam(name: 'RUN_INTEGRATION', defaultValue: true, description: 'Run integration tests')
        booleanParam(name: 'COVERAGE', defaultValue: true, description: 'Generate coverage report')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH}"]],
                    userRemoteConfigs: [[url: "${GIT_REPO_URL}"]]
                ])
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    echo "Setting up Python ${PYTHON_VERSION} environment"
                    sh """
                        python${PYTHON_VERSION} --version
                        python${PYTHON_VERSION} -m venv ${VIRTUAL_ENV}
                        . ${VIRTUAL_ENV}/bin/activate
                        pip install --upgrade pip setuptools wheel
                    """
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing dependencies"
                    sh """
                        . ${VIRTUAL_ENV}/bin/activate
                        pip install -r requirements.txt
                        pip install -r requirements-dev.txt
                    """
                }
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    echo "Running linters"
                    sh """
                        . ${VIRTUAL_ENV}/bin/activate
                        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                        pylint **/*.py || true
                        black --check .
                    """
                }
            }
        }
        
        stage('Type Check') {
            steps {
                script {
                    echo "Running type checker"
                    sh """
                        . ${VIRTUAL_ENV}/bin/activate
                        mypy . || true
                    """
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                script {
                    echo "Running unit tests"
                    sh """
                        . ${VIRTUAL_ENV}/bin/activate
                        pytest tests/unit -v --junitxml=test-results/unit-tests.xml
                    """
                }
            }
        }
        
        stage('Integration Tests') {
            when {
                expression { params.RUN_INTEGRATION == true }
            }
            steps {
                script {
                    echo "Running integration tests"
                    sh """
                        . ${VIRTUAL_ENV}/bin/activate
                        pytest tests/integration -v --junitxml=test-results/integration-tests.xml
                    """
                }
            }
        }
        
        stage('Coverage Report') {
            when {
                expression { params.COVERAGE == true }
            }
            steps {
                script {
                    echo "Generating coverage report"
                    sh """
                        . ${VIRTUAL_ENV}/bin/activate
                        pytest --cov=. --cov-report=html --cov-report=xml
                    """
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    echo "Running security scan"
                    sh """
                        . ${VIRTUAL_ENV}/bin/activate
                        bandit -r . -f json -o bandit-report.json || true
                        safety check --json || true
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "All tests passed!"
            junit 'test-results/**/*.xml'
        }
        failure {
            echo "Tests failed!"
        }
        always {
            cleanWs()
        }
    }
}
