pipeline {
    agent any
    
    environment {
        HELM_VERSION = "3.13.0"
        KUBECONFIG = credentials('kubeconfig-credentials-id')
        CHART_PATH = "helm-chart"
        RELEASE_NAME = "${APP_NAME}"
        NAMESPACE = "${K8S_NAMESPACE}"
    }
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Target environment')
        string(name: 'CHART_VERSION', defaultValue: 'latest', description: 'Chart version')
        booleanParam(name: 'DRY_RUN', defaultValue: false, description: 'Perform dry run')
        booleanParam(name: 'ROLLBACK', defaultValue: false, description: 'Rollback to previous release')
    }
    
    stages {
        stage('Setup Helm') {
            steps {
                script {
                    echo "Setting up Helm ${HELM_VERSION}"
                    sh """
                        wget -q https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz
                        tar -zxf helm-v${HELM_VERSION}-linux-amd64.tar.gz
                        chmod +x linux-amd64/helm
                        ./linux-amd64/helm version
                    """
                }
            }
        }
        
        stage('Validate Kubernetes Connection') {
            steps {
                script {
                    echo "Validating Kubernetes connection"
                    sh """
                        kubectl cluster-info
                        kubectl get nodes
                    """
                }
            }
        }
        
        stage('Lint Helm Chart') {
            steps {
                script {
                    echo "Linting Helm chart"
                    sh "./linux-amd64/helm lint ${CHART_PATH}"
                }
            }
        }
        
        stage('Helm Rollback') {
            when {
                expression { params.ROLLBACK == true }
            }
            steps {
                script {
                    echo "Rolling back release"
                    sh """
                        ./linux-amd64/helm rollback ${RELEASE_NAME} -n ${NAMESPACE}
                        ./linux-amd64/helm status ${RELEASE_NAME} -n ${NAMESPACE}
                    """
                }
            }
        }
        
        stage('Helm Deploy') {
            when {
                expression { params.ROLLBACK == false }
            }
            steps {
                script {
                    def dryRunFlag = params.DRY_RUN ? '--dry-run' : ''
                    echo "Deploying Helm chart to ${params.ENVIRONMENT}"
                    sh """
                        ./linux-amd64/helm upgrade --install ${RELEASE_NAME} ${CHART_PATH} \
                            --namespace ${NAMESPACE} \
                            --create-namespace \
                            --values ${CHART_PATH}/values-${params.ENVIRONMENT}.yaml \
                            --set image.tag=${params.CHART_VERSION} \
                            --wait \
                            --timeout 10m \
                            ${dryRunFlag}
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            when {
                expression { params.DRY_RUN == false && params.ROLLBACK == false }
            }
            steps {
                script {
                    echo "Verifying deployment"
                    sh """
                        ./linux-amd64/helm status ${RELEASE_NAME} -n ${NAMESPACE}
                        ./linux-amd64/helm get values ${RELEASE_NAME} -n ${NAMESPACE}
                        kubectl get all -n ${NAMESPACE} -l app.kubernetes.io/instance=${RELEASE_NAME}
                    """
                }
            }
        }
        
        stage('Run Tests') {
            when {
                expression { params.DRY_RUN == false }
            }
            steps {
                script {
                    echo "Running Helm tests"
                    sh "./linux-amd64/helm test ${RELEASE_NAME} -n ${NAMESPACE} || true"
                }
            }
        }
        
        stage('Release History') {
            steps {
                script {
                    echo "Helm release history"
                    sh "./linux-amd64/helm history ${RELEASE_NAME} -n ${NAMESPACE}"
                }
            }
        }
    }
    
    post {
        success {
            echo "Helm deployment successful!"
            slackSend(color: 'good', message: "Helm Deploy Success: ${RELEASE_NAME} to ${params.ENVIRONMENT}")
        }
        failure {
            echo "Helm deployment failed!"
            slackSend(color: 'danger', message: "Helm Deploy Failed: ${RELEASE_NAME} to ${params.ENVIRONMENT}")
        }
        always {
            cleanWs()
        }
    }
}
