pipeline {
    agent any
    
    environment {
        AWS_CREDENTIALS = credentials('aws-credentials-id')
        TF_VERSION = "1.6.0"
        TF_WORKSPACE = "${ENVIRONMENT}"
        TF_DIR = "terraform"
    }
    
    parameters {
        choice(name: 'ACTION', choices: ['plan', 'apply', 'destroy'], description: 'Terraform action')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Target environment')
        booleanParam(name: 'AUTO_APPROVE', defaultValue: false, description: 'Auto approve apply/destroy')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Terraform') {
            steps {
                script {
                    echo "Setting up Terraform ${TF_VERSION}"
                    sh """
                        wget -q https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip
                        unzip -o terraform_${TF_VERSION}_linux_amd64.zip
                        chmod +x terraform
                        ./terraform version
                    """
                }
            }
        }
        
        stage('Terraform Init') {
            steps {
                script {
                    echo "Initializing Terraform"
                    dir(TF_DIR) {
                        sh """
                            ../terraform init -backend-config="key=${ENVIRONMENT}/terraform.tfstate"
                            ../terraform workspace select ${TF_WORKSPACE} || ../terraform workspace new ${TF_WORKSPACE}
                        """
                    }
                }
            }
        }
        
        stage('Terraform Validate') {
            steps {
                script {
                    echo "Validating Terraform configuration"
                    dir(TF_DIR) {
                        sh "../terraform validate"
                    }
                }
            }
        }
        
        stage('Terraform Plan') {
            steps {
                script {
                    echo "Running Terraform plan"
                    dir(TF_DIR) {
                        sh """
                            ../terraform plan \
                                -var-file="${ENVIRONMENT}.tfvars" \
                                -out=tfplan
                        """
                    }
                }
            }
        }
        
        stage('Terraform Apply') {
            when {
                expression { params.ACTION == 'apply' }
            }
            steps {
                script {
                    if (params.AUTO_APPROVE) {
                        echo "Applying Terraform changes (auto-approved)"
                        dir(TF_DIR) {
                            sh "../terraform apply -auto-approve tfplan"
                        }
                    } else {
                        input message: 'Approve Terraform Apply?', ok: 'Apply'
                        echo "Applying Terraform changes"
                        dir(TF_DIR) {
                            sh "../terraform apply tfplan"
                        }
                    }
                }
            }
        }
        
        stage('Terraform Destroy') {
            when {
                expression { params.ACTION == 'destroy' }
            }
            steps {
                script {
                    if (params.AUTO_APPROVE) {
                        echo "Destroying Terraform resources (auto-approved)"
                        dir(TF_DIR) {
                            sh """
                                ../terraform destroy \
                                    -var-file="${ENVIRONMENT}.tfvars" \
                                    -auto-approve
                            """
                        }
                    } else {
                        input message: 'Approve Terraform Destroy?', ok: 'Destroy'
                        echo "Destroying Terraform resources"
                        dir(TF_DIR) {
                            sh """
                                ../terraform destroy \
                                    -var-file="${ENVIRONMENT}.tfvars"
                            """
                        }
                    }
                }
            }
        }
        
        stage('Terraform Output') {
            when {
                expression { params.ACTION != 'destroy' }
            }
            steps {
                script {
                    echo "Terraform outputs:"
                    dir(TF_DIR) {
                        sh "../terraform output"
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo "Terraform ${params.ACTION} completed successfully"
        }
        failure {
            echo "Terraform ${params.ACTION} failed"
        }
        always {
            cleanWs()
        }
    }
}
