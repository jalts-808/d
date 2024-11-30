pipeline {
    agent any
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
                sh 'python3 --version || python --version'
                sh 'python3 -m pip --version || python -m pip --version'
                sh 'python3 -m venv venv || python -m venv venv'
                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Setup Media Directory') {
            steps {
                echo 'Creating media directory...'
                sh 'mkdir -p media/uploads/products'
            }
        }
        stage('Migrate Database') {
            steps {
                echo 'Running database migrations...'
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH=$PYTHONPATH:$WORKSPACE/ecom
                    export DJANGO_SETTINGS_MODULE=ecom.settings
                    python manage.py makemigrations
                    python manage.py migrate
                '''
            }
        }
        stage('Seed Database') {
            steps {
                echo 'Starting Seed Database Stage...'
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH=$PYTHONPATH:$WORKSPACE/ecom
                    export DJANGO_SETTINGS_MODULE=ecom.settings
                    echo PYTHONPATH: $PYTHONPATH
                    echo DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE
                    python scripts/seed_db.py
                '''
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Starting Run Tests Stage...'
                sh '''
                    . venv/bin/activate
                    pytest --junitxml=pytest_report.xml --maxfail=5 --disable-warnings
                '''
                sh 'ls -la pytest_report.xml'
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
                def testReport = fileExists('pytest_report.xml')
                if (testReport) {
                    junit 'pytest_report.xml'
                } else {
                    echo 'No test report found. Skipping JUnit reporting.'
                }
            }
        }
    }
}
