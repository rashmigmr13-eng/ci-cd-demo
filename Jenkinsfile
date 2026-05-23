pipeline {
    agent any

    environment {
        SSH_KEY = "/var/lib/jenkins/.ssh/id_ed25519"
        DEV_SERVER  = "ubuntu@13.229.239.70"
        TEST_SERVER = "ubuntu@13.250.55.218"
        PROD_SERVER = "ubuntu@13.212.104.46"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rashmigmr13-eng/ci-cd-demo.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy DEV') {
            steps {
                sh """
                rsync -avz -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \
                --exclude venv ./ ${DEV_SERVER}:/home/ubuntu/app/

                ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${DEV_SERVER} "
                    cd /home/ubuntu/app &&
                    python3 -m venv venv &&
                    . venv/bin/activate &&
                    pip install -r requirements.txt &&
                    nohup python3 app.py > app.log 2>&1 &
                "
                """
            }
        }

        stage('Deploy TEST') {
            steps {
                input message: "Approve deployment to TEST?"
                sh """
                rsync -avz -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \
                --exclude venv ./ ${TEST_SERVER}:/home/ubuntu/app/

                ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${TEST_SERVER} "
                    cd /home/ubuntu/app &&
                    python3 -m venv venv &&
                    . venv/bin/activate &&
                    pip install -r requirements.txt &&
                    nohup python3 app.py > app.log 2>&1 &
                "
                """
            }
        }

        stage('Deploy PROD') {
            steps {
                input message: "Approve deployment to PROD?"
                sh """
                rsync -avz -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \
                --exclude venv ./ ${PROD_SERVER}:/home/ubuntu/app/

                ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${PROD_SERVER} "
                    cd /home/ubuntu/app &&
                    python3 -m venv venv &&
                    . venv/bin/activate &&
                    pip install -r requirements.txt &&
                    nohup python3 app.py > app.log 2>&1 &
                "
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS ✅"
        }
        failure {
            echo "Pipeline FAILED ❌"
        }
    }
}
