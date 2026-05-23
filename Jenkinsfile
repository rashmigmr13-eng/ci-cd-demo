pipeline {
    agent any

    environment {
        DEV_SERVER = "13.229.239.70"
    }

    stages {

        stage('Clone Code') {
            steps {
                git 'https://github.com/rashmigmr13-eng/ci-cd-demo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy to Dev') {
            steps {
                sh '''
                ssh ubuntu@$DEV_SERVER "mkdir -p /home/ubuntu/app"

                scp -r * ubuntu@$DEV_SERVER:/home/ubuntu/app/

                ssh ubuntu@$DEV_SERVER "
                    pkill -f app.py || true
                    cd /home/ubuntu/app
                    nohup python3 app.py > output.log 2>&1 &
                "
                '''
            }
        }
    }
}
