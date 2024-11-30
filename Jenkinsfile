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
        stage('Seed Database') {
            steps {
                sh '. venv/bin/activate && python ecom/scripts/seed_db.py' // Updated path
            }
        }
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest ecom/cart/tests --junitxml=pytest_report.xml --maxfail=5 --disable-warnings' // Updated path
            }
        }
    }
    post {
        always {
            junit 'pytest_report.xml' // Publish the test results
        }
    }
}
