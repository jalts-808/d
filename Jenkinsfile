pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Starting Checkout Stage...'
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Starting Install Dependencies Stage...'
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Seed Database') {
            steps {
                echo 'Starting Seed Database Stage...'
                sh '. venv/bin/activate && python scripts/seed_db.py'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Starting Run Tests Stage...'
                sh '. venv/bin/activate && pytest --junitxml=pytest_report.xml --maxfail=5 --disable-warnings'
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
