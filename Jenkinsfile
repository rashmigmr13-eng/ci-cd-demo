pipeline {
    agent any

    stages {

        stage('Clone Code') {
            steps {
                git 'YOUR_GITHUB_REPO'
            }
        }

        stage('Build') {
            steps {
                sh 'echo Build Successful'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'echo Running Tests'
            }
        }

        stage('Deploy Dev') {
            steps {
                sh 'echo Deploying to Dev Server'
            }
        }
    }
}
