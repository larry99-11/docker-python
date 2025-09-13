pipeline {
    agent any


    // This section defines the trigger. This is SCM Polling, which tells Jenkins to check
    // for changes in your repository every minute.
    // NOTE: For a real-time, event-based trigger, you would use a webhook instead.
    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Pull Code') {
            steps {
                // This step checks out the code from your Git repository.
                git branch: 'master', url: 'https://github.com/larry99-11/docker-python.git'
            }
        }
        
        stage('Build and Deploy') {
            steps {

                // accessing secrets via withCredentials
                withCredentials([
                    string(credentialsId: 'DB_USER_ID', variable: 'DB_USER'),
                    string(credentialsId: 'DB_PASS_ID', variable: 'DB_PASS'),
                    string(credentialsId: 'DB_NAME_ID', variable: 'DB_NAME')
                ]){
                // This script block runs shell commands directly on the Jenkins agent
                // (in my case, the Raspberry Pi).
                sh 'docker compose -f docker-compose.yml up -d --build --force-recreate'
                }
            }
        }
    }
}
