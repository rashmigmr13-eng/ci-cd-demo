pipeline {

    agent any

    environment {

        DEV_SERVER  = "ubuntu@13.229.239.70"
        TEST_SERVER = "ubuntu@13.250.55.218"
        PROD_SERVER = "ubuntu@13.212.104.46"

        APP_DIR = "/home/ubuntu/app"
    }

    stages {

        // =========================
        // CLONE CODE
        // =========================

        stage('Clone Code') {

            steps {

                git branch: 'main',
                url: 'https://github.com/rashmigmr13-eng/ci-cd-demo.git'
            }
        }

        // =========================
        // BUILD
        // =========================

        stage('Build') {

            steps {

                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        // =========================
        // DEPLOY TO DEV SERVER
        // =========================

        stage('Deploy DEV') {

            steps {

                sh """

                    rsync -avz --exclude 'venv' ./ $DEV_SERVER:$APP_DIR/

                    ssh $DEV_SERVER '

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

        // =========================
        // DEPLOY TO TEST SERVER
        // =========================

        stage('Deploy TEST') {

            steps {

                sh """

                    rsync -avz --exclude 'venv' ./ $TEST_SERVER:$APP_DIR/

                    ssh $TEST_SERVER '

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

        // =========================
        // TESTING ON TEST SERVER
        // =========================

        stage('Testing') {

            steps {

                sh """

                    ssh $TEST_SERVER '

                        curl http://localhost:5000

                    '
                """
            }
        }

        // =========================
        // MANUAL APPROVAL
        // =========================

        stage('Approval') {

            steps {

                input 'Deploy to Production?'
            }
        }

        // =========================
        // DEPLOY TO PROD SERVER
        // =========================

        stage('Deploy PROD') {

            steps {

                sh """

                    rsync -avz --exclude 'venv' ./ $PROD_SERVER:$APP_DIR/

                    ssh $PROD_SERVER '

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

            echo 'Pipeline Successful!'
        }

        failure {

            echo 'Pipeline Failed!'
        }
    }
}
