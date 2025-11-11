pipeline {
    agent any
    
    environment {
        KUBECONFIG = credentials('kubeconfig-credentials-id')
        NAMESPACE = "${K8S_NAMESPACE}"
        DEPLOYMENT_NAME = "${APP_NAME}"
        IMAGE_NAME = "${DOCKER_REGISTRY}/${APP_NAME}"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Target environment')
        string(name: 'REPLICAS', defaultValue: '3', description: 'Number of replicas')
        booleanParam(name: 'ROLLBACK', defaultValue: false, description: 'Rollback to previous version')
    }
    
    stages {
        stage('Validate Kubernetes Connection') {
            steps {
                script {
                    echo "Validating connection to Kubernetes cluster"
                    sh """
                        kubectl cluster-info
                        kubectl get nodes
                    """
                }
            }
        }
        
        stage('Rollback') {
            when {
                expression { params.ROLLBACK == true }
            }
            steps {
                script {
                    echo "Rolling back deployment"
                    sh """
                        kubectl rollout undo deployment/${DEPLOYMENT_NAME} -n ${NAMESPACE}
                        kubectl rollout status deployment/${DEPLOYMENT_NAME} -n ${NAMESPACE}
                    """
                }
            }
        }
        
        stage('Update Deployment') {
            when {
                expression { params.ROLLBACK == false }
            }
            steps {
                script {
                    echo "Updating deployment with image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh """
                        kubectl set image deployment/${DEPLOYMENT_NAME} \
                            ${DEPLOYMENT_NAME}=${IMAGE_NAME}:${IMAGE_TAG} \
                            -n ${NAMESPACE} \
                            --record
                        
                        kubectl scale deployment/${DEPLOYMENT_NAME} \
                            --replicas=${params.REPLICAS} \
                            -n ${NAMESPACE}
                    """
                }
            }
        }
        
        stage('Wait for Rollout') {
            when {
                expression { params.ROLLBACK == false }
            }
            steps {
                script {
                    echo "Waiting for rollout to complete"
                    sh """
                        kubectl rollout status deployment/${DEPLOYMENT_NAME} \
                            -n ${NAMESPACE} \
                            --timeout=5m
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo "Verifying deployment"
                    sh """
                        kubectl get deployment ${DEPLOYMENT_NAME} -n ${NAMESPACE}
                        kubectl get pods -l app=${DEPLOYMENT_NAME} -n ${NAMESPACE}
                        kubectl describe deployment ${DEPLOYMENT_NAME} -n ${NAMESPACE}
                    """
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo "Running health checks"
                    sh """
                        sleep 30
                        kubectl get pods -l app=${DEPLOYMENT_NAME} -n ${NAMESPACE} -o json | \
                            jq -r '.items[] | select(.status.phase != "Running") | .metadata.name' | \
                            while read pod; do
                                echo "Pod \$pod is not running"
                                kubectl logs \$pod -n ${NAMESPACE} --tail=50
                            done
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "Deployment successful!"
            slackSend(color: 'good', message: "Deployment Success: ${DEPLOYMENT_NAME} to ${params.ENVIRONMENT}")
        }
        failure {
            echo "Deployment failed!"
            slackSend(color: 'danger', message: "Deployment Failed: ${DEPLOYMENT_NAME} to ${params.ENVIRONMENT}")
        }
    }
}
