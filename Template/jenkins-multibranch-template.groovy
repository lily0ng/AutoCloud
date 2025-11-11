pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    echo "Building branch: ${env.BRANCH_NAME}"
                    sh "npm install"
                    sh "npm run build"
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh "npm test"
                }
            }
        }
        
        stage('Deploy to Dev') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    echo "Deploying to dev environment"
                    sh "./deploy.sh dev"
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'staging'
            }
            steps {
                script {
                    echo "Deploying to staging environment"
                    sh "./deploy.sh staging"
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                script {
                    echo "Deploying to production environment"
                    sh "./deploy.sh prod"
                }
            }
        }
    }
    
    post {
        success {
            echo "Pipeline completed successfully"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}
