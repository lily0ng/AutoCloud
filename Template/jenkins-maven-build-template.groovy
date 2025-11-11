pipeline {
    agent any
    
    tools {
        maven 'Maven-3.9'
        jdk 'JDK-17'
    }
    
    environment {
        MAVEN_OPTS = "-Xmx1024m"
    }
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
        choice(name: 'PROFILE', choices: ['dev', 'staging', 'prod'], description: 'Maven profile')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip tests')
        booleanParam(name: 'DEPLOY_ARTIFACTS', defaultValue: false, description: 'Deploy to artifact repository')
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
        
        stage('Build Info') {
            steps {
                script {
                    echo "Maven version:"
                    sh "mvn --version"
                    echo "Java version:"
                    sh "java -version"
                }
            }
        }
        
        stage('Compile') {
            steps {
                script {
                    echo "Compiling project"
                    sh "mvn clean compile -P${params.PROFILE}"
                }
            }
        }
        
        stage('Unit Tests') {
            when {
                expression { params.SKIP_TESTS == false }
            }
            steps {
                script {
                    echo "Running unit tests"
                    sh "mvn test -P${params.PROFILE}"
                }
            }
        }
        
        stage('Integration Tests') {
            when {
                expression { params.SKIP_TESTS == false }
            }
            steps {
                script {
                    echo "Running integration tests"
                    sh "mvn verify -P${params.PROFILE}"
                }
            }
        }
        
        stage('Code Quality Analysis') {
            steps {
                script {
                    echo "Running SonarQube analysis"
                    withSonarQubeEnv('SonarQube') {
                        sh "mvn sonar:sonar -P${params.PROFILE}"
                    }
                }
            }
        }
        
        stage('Package') {
            steps {
                script {
                    echo "Packaging application"
                    if (params.SKIP_TESTS) {
                        sh "mvn package -DskipTests -P${params.PROFILE}"
                    } else {
                        sh "mvn package -P${params.PROFILE}"
                    }
                }
            }
        }
        
        stage('Deploy Artifacts') {
            when {
                expression { params.DEPLOY_ARTIFACTS == true }
            }
            steps {
                script {
                    echo "Deploying artifacts to repository"
                    sh "mvn deploy -DskipTests -P${params.PROFILE}"
                }
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                script {
                    echo "Archiving artifacts"
                    archiveArtifacts artifacts: '**/target/*.jar,**/target/*.war', fingerprint: true
                }
            }
        }
    }
    
    post {
        success {
            echo "Build successful!"
            junit '**/target/surefire-reports/*.xml'
        }
        failure {
            echo "Build failed!"
        }
        always {
            cleanWs()
        }
    }
}
