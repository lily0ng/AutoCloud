pipeline {
    agent any
    
    environment {
        ANSIBLE_VERSION = "2.15"
        ANSIBLE_CONFIG = "${WORKSPACE}/ansible.cfg"
        INVENTORY_PATH = "inventory"
        PLAYBOOK_PATH = "playbooks"
    }
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Target environment')
        choice(name: 'PLAYBOOK', choices: ['deploy.yml', 'rollback.yml', 'configure.yml'], description: 'Playbook to run')
        string(name: 'TAGS', defaultValue: '', description: 'Ansible tags')
        booleanParam(name: 'CHECK_MODE', defaultValue: false, description: 'Run in check mode')
    }
    
    stages {
        stage('Setup Ansible') {
            steps {
                script {
                    sh """
                        pip3 install ansible==${ANSIBLE_VERSION}
                        ansible --version
                    """
                }
            }
        }
        
        stage('Run Playbook') {
            steps {
                script {
                    def checkFlag = params.CHECK_MODE ? '--check' : ''
                    def tagsFlag = params.TAGS ? "--tags ${params.TAGS}" : ''
                    sh """
                        ansible-playbook ${PLAYBOOK_PATH}/${params.PLAYBOOK} \
                            -i ${INVENTORY_PATH}/${params.ENVIRONMENT} \
                            ${checkFlag} ${tagsFlag}
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
