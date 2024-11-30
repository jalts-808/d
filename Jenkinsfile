pipeline {
    agent any
    stages {
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
        stage('Seed Database') {
            steps {
                echo 'Starting Seed Database Stage...'
                sh 'pwd'
                sh 'ls -R'
                sh '''
                    . venv/bin/activate
                    python scripts/seed_db.py
                '''
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Starting Run Tests Stage...'
                sh 'pwd'
                sh 'ls -R'
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
            echo 'Publishing test results...'
            junit 'pytest_report.xml'
        }
    }
}
