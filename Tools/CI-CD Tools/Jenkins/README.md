# Jenkins Configuration Guide

## Table of Contents
1. [Jenkins Installation and Setup](#installation)
2. [Docker Integration](#docker)
3. [AWS Integration](#aws)
4. [Kubernetes Integration](#kubernetes)
5. [Pipeline Automation](#automation)
6. [Best Practices](#best-practices)

## Installation

### Prerequisites
- Java 11 or Java 17 (LTS)
- 4GB+ RAM
- 50GB+ free disk space
- Docker installed (for containerized setup)

### Docker-based Installation
```bash
docker run -d \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins \
  jenkins/jenkins:lts
```

### Initial Setup
1. Get initial admin password:
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
2. Access Jenkins at http://localhost:8080
3. Install suggested plugins
4. Create admin user

## Docker Integration

### Configure Docker in Jenkins
1. Install Docker plugins:
   - Docker
   - Docker Pipeline
   - Docker API

2. Configure Docker agent template:
```groovy
pipeline {
    agent {
        docker {
            image 'node:16'
            args '-v $HOME/.m2:/root/.m2'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
    }
}
```

## AWS Integration

### Setup AWS Credentials
1. Install AWS plugins:
   - AWS Credentials
   - AWS Steps
   - Pipeline: AWS Steps

2. Configure AWS Credentials:
   - Go to Manage Jenkins > Manage Credentials
   - Add AWS credentials (Access Key and Secret Key)

3. Example AWS Pipeline:
```groovy
pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'
    }
    stages {
        stage('Deploy to AWS') {
            steps {
                withAWS(credentials: 'aws-credentials-id', region: env.AWS_REGION) {
                    sh 'aws s3 cp build/ s3://my-bucket/ --recursive'
                }
            }
        }
    }
}
```

## Kubernetes Integration

### Setup Kubernetes
1. Install Kubernetes plugins:
   - Kubernetes
   - Kubernetes CLI

2. Configure Kubernetes Cloud:
   - Add Kubernetes cloud configuration
   - Set up service account and credentials

3. Example Kubernetes Deployment Pipeline:
```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: maven
                    image: maven:3.8.1-jdk-11
                    command:
                    - cat
                    tty: true
            '''
        }
    }
    stages {
        stage('Build and Deploy') {
            steps {
                container('maven') {
                    sh 'mvn clean package'
                    sh 'kubectl apply -f k8s/'
                }
            }
        }
    }
}
```

## Pipeline Automation

### Automated CI/CD Pipeline
```groovy
pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        APP_NAME = 'your-app'
        AWS_REGION = 'us-east-1'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm run test'
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry('https://${DOCKER_REGISTRY}', 'registry-credentials') {
                        docker.image("${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}").push()
                    }
                }
            }
        }
        
        stage('Deploy to K8s') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh """
                        kubectl set image deployment/${APP_NAME} \
                        ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}
                    """
                }
            }
        }
    }
    
    post {
        success {
            slackSend channel: '#deployments',
                      color: 'good',
                      message: "Deployment successful: ${APP_NAME} - Build #${BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#deployments',
                      color: 'danger',
                      message: "Deployment failed: ${APP_NAME} - Build #${BUILD_NUMBER}"
        }
    }
}
```

## Best Practices

### Security
1. Use credentials management for sensitive data
2. Implement role-based access control (RBAC)
3. Regular security updates
4. Use secure plugins

### Performance
1. Clean up old builds
2. Use agent-based builds
3. Optimize pipeline steps
4. Use parallel execution when possible

### Monitoring
1. Set up email notifications
2. Configure build monitors
3. Use logging and monitoring plugins
4. Set up alerts for failed builds

### Backup
1. Regular Jenkins home backup
2. Configuration backup
3. Plugin state backup
4. Disaster recovery plan
