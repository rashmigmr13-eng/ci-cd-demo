pipeline {
    agent any

    environment {
        DEV_SERVER  = "ubuntu@13.229.239.70"
        TEST_SERVER = "ubuntu@13.250.55.218"
        PROD_SERVER = "ubuntu@13.212.104.46"

        APP_DIR = "/home/ubuntu/app"
        SSH_KEY = "/root/.ssh/id_ed25519"
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
                    pip install -r requirements.txt
                '''
            }
        }

        // ================= DEV =================
        stage('Deploy DEV') {
            steps {
                sh """
                    rsync -avz -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
                    --exclude 'venv' ./ $DEV_SERVER:$APP_DIR/

                    ssh -i $SSH_KEY -o StrictHostKeyChecking=no $DEV_SERVER '
                        pkill -f app.py || true
                        cd $APP_DIR
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        nohup python3 app.py > app.log 2>&1 &
                    '
                """
            }
        }

        // ================= TEST =================
        stage('Deploy TEST') {
            steps {
                sh """
                    rsync -avz -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
                    --exclude 'venv' ./ $TEST_SERVER:$APP_DIR/

                    ssh -i $SSH_KEY -o StrictHostKeyChecking=no $TEST_SERVER '
                        pkill -f app.py || true
                        cd $APP_DIR
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        nohup python3 app.py > app.log 2>&1 &
                    '
                """
            }
        }

        stage('Testing') {
            steps {
                sh """
                    ssh -i $SSH_KEY -o StrictHostKeyChecking=no $TEST_SERVER '
                        curl http://localhost:5000
                    '
                """
            }
        }

        // ================= APPROVAL =================
        stage('Approval') {
            steps {
                input message: 'Deploy to Production?'
            }
        }

        // ================= PROD =================
        stage('Deploy PROD') {
            steps {
                sh """
                    rsync -avz -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
                    --exclude 'venv' ./ $PROD_SERVER:$APP_DIR/

                    ssh -i $SSH_KEY -o StrictHostKeyChecking=no $PROD_SERVER '
                        pkill -f app.py || true
                        cd $APP_DIR
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        nohup python3 app.py > app.log 2>&1 &
                    '
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline Successful 🚀"
        }
        failure {
            echo "Pipeline Failed ❌"
        }
    }
}
