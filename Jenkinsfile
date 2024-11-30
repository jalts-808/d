pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Starting Checkout Stage...'
                checkout scm
                sh 'pwd'
                sh 'ls -la'
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Starting Install Dependencies Stage...'
                sh 'python --version'
                sh 'python -m pip --version'
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Seed Database') {
            steps {
                echo 'Starting Seed Database Stage...'
                sh 'pwd'
                sh 'ls -la'
                sh '. venv/bin/activate && python scripts/seed_db.py'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Starting Run Tests Stage...'
                sh 'pwd'
                sh 'ls -la'
                sh '. venv/bin/activate && pytest --junitxml=pytest_report.xml --maxfail=5 --disable-warnings'
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
