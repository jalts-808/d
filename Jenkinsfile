pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Prepare Database') {
            steps {
                sh '. venv/bin/activate && python manage.py migrate'
            }
        }
        stage('Seed Database') {
            steps {
                sh '. venv/bin/activate && python manage.py shell < scripts/seed_db.py'
            }
        }
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest --junitxml=pytest_report.xml --maxfail=5 --disable-warnings'
            }
        }
        stage('Publish Test Results') {
            steps {
                junit 'pytest_report.xml'
            }
        }
    }
}
