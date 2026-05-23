pipeline {

    agent any

    environment {

        DEV_SERVER  = "ubuntu@13.229.239.70"
        TEST_SERVER = "ubuntu@13.250.55.218"
        PROD_SERVER = "ubuntu@13.212.104.46"

        APP_DIR = "/home/ubuntu/app"
    }

    stages {

        stage('Clone Code') {

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

        stage('Unit Test') {

            steps {

                sh '''
                    . venv/bin/activate
                    python -m unittest discover || true
                '''
            }
        }

        stage('Archive Artifacts') {

            steps {

                archiveArtifacts artifacts: '**/*'
            }
        }

        stage('Deploy DEV') {

            steps {

                sh """

                    ssh $DEV_SERVER '
                        mkdir -p $APP_DIR
                    '

                    scp -r * $DEV_SERVER:$APP_DIR

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

        stage('DEV Testing') {

            steps {

                sh """

                    ssh $DEV_SERVER '

                        curl -I http://localhost:5000

                    '
                """
            }
        }

        stage('Deploy TEST') {

            steps {

                sh """

                    ssh $TEST_SERVER '
                        mkdir -p $APP_DIR
                    '

                    scp -r * $TEST_SERVER:$APP_DIR

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

        stage('QA Testing') {

            steps {

                sh """

                    ssh $TEST_SERVER '

                        curl -I http://localhost:5000

                    '
                """
            }
        }

        stage('Manual Approval') {

            steps {

                input 'Deploy to Production?'
            }
        }

        stage('Deploy PROD') {

            steps {

                sh """

                    ssh $PROD_SERVER '
                        mkdir -p $APP_DIR
                    '

                    scp -r * $PROD_SERVER:$APP_DIR

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

            echo 'Pipeline Executed Successfully!'
        }

        failure {

            echo 'Pipeline Failed!'
        }
    }
}
