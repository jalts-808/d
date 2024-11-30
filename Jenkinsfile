pipeline {
    agent any
    environment {
        DJANGO_SETTINGS_MODULE = 'ecom.settings'
        PYTHONPATH = "${WORKSPACE}/ecom"
    }
    stages {
        stage('Debug Start') {
            steps {
                echo 'Starting Debugging Stage at the Beginning...'
                sh 'echo "Current PATH: $PATH"'
                sh 'python3 --version || python --version'
                sh 'python3 -m pip --version || python -m pip --version'
                sh 'env'
                sh 'echo PYTHONPATH: $PYTHONPATH'
                sh 'echo DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE'
            }
        }
        stage('Checkout') {
            steps {
                echo 'Starting Checkout Stage...'
                checkout scm
                sh 'pwd'
                sh 'ls -R'
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Starting Install Dependencies Stage...'
                sh '''
                    python3 --version || python --version
                    python3 -m pip --version || python -m pip --version
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Verify pytest Installation') {
            steps {
                echo 'Verifying pytest Installation...'
                sh '''
                    . venv/bin/activate
                    pytest --version
                '''
            }
        }
        stage('Setup Media Directory') {
            steps {
                echo 'Creating media directory...'
                sh 'mkdir -p ecom/media/uploads/products'
            }
        }
        stage('Migrate Database') {
            steps {
                echo 'Running database migrations...'
                sh '''
                    . venv/bin/activate
                    python ecom/manage.py makemigrations
                    python ecom/manage.py migrate
                '''
            }
        }
        stage('Seed Database') {
            steps {
                echo 'Starting Seed Database Stage...'
                sh '''
                    . venv/bin/activate
                    echo PYTHONPATH: $PYTHONPATH
                    echo DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE
                    python scripts/seed_db.py
                '''
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Starting Run Tests Stage...'
                script {
                    try {
                        sh '''
                            . venv/bin/activate
                            export PYTHONPATH=$WORKSPACE/ecom
                            echo "PYTHONPATH: $PYTHONPATH"
                            echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
                            pytest --ds=ecom.settings --junitxml=pytest_report.xml --maxfail=5 --disable-warnings
                        '''
                    } catch (Exception e) {
                        echo "Tests failed but build will continue."
                    }
                }
                sh 'ls -la pytest_report.xml || echo "Test report not found!"'
            }
        }
        stage('Run Payment Tests') { // New stage
            steps {
                echo 'Running Payment App Tests...'
                script {
                    try {
                        sh '''
                            . venv/bin/activate
                            export PYTHONPATH=$WORKSPACE/ecom
                            echo "PYTHONPATH: $PYTHONPATH"
                            echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
                            pytest ecom/payment/tests/test_payment.py --ds=ecom.settings --junitxml=pytest_payment_report.xml --maxfail=5 --disable-warnings
                        '''
                    } catch (Exception e) {
                        echo "Payment tests failed but build will continue."
                    }
                }
                sh 'ls -la pytest_payment_report.xml || echo "Payment test report not found!"'
            }
        }
    }
    post {
        always {
            echo 'Starting Debugging Stage at the End...'
            sh 'echo "Final PATH: $PATH"'
            sh 'python3 --version || python --version'
            sh 'python3 -m pip --version || python -m pip --version'
            sh 'env'
            sh 'echo PYTHONPATH: $PYTHONPATH'
            sh 'echo DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE'
            echo 'Publishing test results...'
            script {
                def mainTestReport = fileExists('pytest_report.xml')
                if (mainTestReport) {
                    junit 'pytest_report.xml'
                } else {
                    echo 'No test report found for main tests. Skipping JUnit reporting.'
                }

                def paymentTestReport = fileExists('pytest_payment_report.xml')
                if (paymentTestReport) {
                    junit 'pytest_payment_report.xml'
                } else {
                    echo 'No test report found for payment tests. Skipping JUnit reporting.'
                }
            }
        }
    }
}
