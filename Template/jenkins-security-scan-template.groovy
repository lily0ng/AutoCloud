pipeline {
    agent any
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch')
        booleanParam(name: 'SAST', defaultValue: true, description: 'Run SAST scan')
        booleanParam(name: 'DEPENDENCY', defaultValue: true, description: 'Run dependency scan')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('SAST Scan') {
            when {
                expression { params.SAST == true }
            }
            steps {
                script {
                    sh """
                        docker run --rm -v \${PWD}:/src returntocorp/semgrep semgrep --config=auto /src
                    """
                }
            }
        }
        
        stage('Dependency Scan') {
            when {
                expression { params.DEPENDENCY == true }
            }
            steps {
                script {
                    sh "npm audit || true"
                }
            }
        }
        
        stage('Container Scan') {
            steps {
                script {
                    sh """
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image ${IMAGE_NAME}
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
