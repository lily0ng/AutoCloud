pipeline {
    agent any
    
    tools {
        nodejs "NodeJS-18"
    }
    
    environment {
        NODE_ENV = "test"
        CI = "true"
    }
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to test')
        booleanParam(name: 'RUN_E2E', defaultValue: false, description: 'Run E2E tests')
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
        
        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing dependencies"
                    sh """
                        node --version
                        npm --version
                        npm ci
                    """
                }
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    echo "Running linter"
                    sh "npm run lint"
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                script {
                    echo "Running unit tests"
                    if (params.COVERAGE) {
                        sh "npm run test:coverage"
                    } else {
                        sh "npm test"
                    }
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                script {
                    echo "Running integration tests"
                    sh "npm run test:integration"
                }
            }
        }
        
        stage('E2E Tests') {
            when {
                expression { params.RUN_E2E == true }
            }
            steps {
                script {
                    echo "Running E2E tests"
                    sh """
                        npm run test:e2e
                    """
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    echo "Building application"
                    sh "npm run build"
                }
            }
        }
        
        stage('Code Coverage Report') {
            when {
                expression { params.COVERAGE == true }
            }
            steps {
                script {
                    echo "Publishing coverage report"
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo "Running SonarQube analysis"
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            npm run sonar
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo "All tests passed!"
            junit '**/test-results/**/*.xml'
        }
        failure {
            echo "Tests failed!"
        }
        always {
            cleanWs()
        }
    }
}
