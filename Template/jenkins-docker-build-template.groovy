pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = "${DOCKER_REGISTRY_URL}"
        DOCKER_CREDENTIALS = credentials('docker-credentials-id')
        IMAGE_NAME = "${APP_NAME}"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKERFILE_PATH = "Dockerfile"
    }
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Target environment')
        booleanParam(name: 'PUSH_IMAGE', defaultValue: true, description: 'Push image to registry')
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out branch: ${params.BRANCH}"
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${params.BRANCH}"]],
                        userRemoteConfigs: [[
                            url: "${GIT_REPO_URL}",
                            credentialsId: 'git-credentials-id'
                        ]]
                    ])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh """
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} \
                            -f ${DOCKERFILE_PATH} \
                            --build-arg ENVIRONMENT=${params.ENVIRONMENT} \
                            .
                    """
                    
                    // Tag as latest
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    echo "Scanning image for vulnerabilities"
                    sh """
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image --severity HIGH,CRITICAL \
                            ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
        
        stage('Push to Registry') {
            when {
                expression { params.PUSH_IMAGE == true }
            }
            steps {
                script {
                    echo "Pushing image to registry"
                    sh """
                        echo ${DOCKER_CREDENTIALS_PSW} | docker login -u ${DOCKER_CREDENTIALS_USR} --password-stdin ${DOCKER_REGISTRY}
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                        docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    echo "Cleaning up local images"
                    sh """
                        docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
                        docker rmi ${IMAGE_NAME}:latest || true
                        docker rmi ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} || true
                        docker rmi ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest || true
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "Build successful! Image: ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
            slackSend(color: 'good', message: "Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
        failure {
            echo "Build failed!"
            slackSend(color: 'danger', message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
        always {
            cleanWs()
        }
    }
}
