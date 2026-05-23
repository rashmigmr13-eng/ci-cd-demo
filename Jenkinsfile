pipeline {
    agent any

    environment {
        SSH_KEY     = "/var/lib/jenkins/.ssh/id_ed25519"
        DEV_SERVER  = "ubuntu@13.40.55.20"
        TEST_SERVER = "ubuntu@13.40.26.34"
        PROD_SERVER = "ubuntu@16.60.165.86"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/rashmigmr13-eng/ci-cd-demo.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy DEV') {
            steps {
                sh """
                rsync -avz \
                -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \
                --exclude venv ./ ${DEV_SERVER}:/home/ubuntu/app/

                ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${DEV_SERVER} << 'EOF'
                mkdir -p /home/ubuntu/app
                cd /home/ubuntu/app

                pkill -f app.py || true

                echo "ENV=DEV" > .env

                python3 -m venv venv
                . venv/bin/activate

                pip install -r requirements.txt

                nohup python3 app.py > app.log 2>&1 &

                sleep 5
                ps -ef | grep app.py
EOF
                """
            }
        }

        stage('Deploy TEST') {
            steps {
                input message: 'Approve deployment to TEST?'

                sh """
                rsync -avz \
                -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \
                --exclude venv ./ ${TEST_SERVER}:/home/ubuntu/app/

                ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${TEST_SERVER} << 'EOF'
                mkdir -p /home/ubuntu/app
                cd /home/ubuntu/app

                pkill -f app.py || true

                echo "ENV=TEST" > .env

                python3 -m venv venv
                . venv/bin/activate

                pip install -r requirements.txt

                nohup python3 app.py > app.log 2>&1 &

                sleep 5
                ps -ef | grep app.py
EOF
                """
            }
        }

        stage('Deploy PROD') {
            steps {
                input message: 'Approve deployment to PROD?'

                sh """
                rsync -avz \
                -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no" \
                --exclude venv ./ ${PROD_SERVER}:/home/ubuntu/app/

                ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${PROD_SERVER} << 'EOF'
                mkdir -p /home/ubuntu/app
                cd /home/ubuntu/app

                pkill -f app.py || true

                echo "ENV=PROD" > .env

                python3 -m venv venv
                . venv/bin/activate

                pip install -r requirements.txt

                nohup python3 app.py > app.log 2>&1 &

                sleep 5
                ps -ef | grep app.py
EOF
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS ✅'
        }

        failure {
            echo 'Pipeline FAILED ❌'
        }
    }
}
