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
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest --maxfail=5 --disable-warnings --junitxml=pytest_report.xml'
                junit 'pytest_report.xml' // Publish JUnit report
            }
        }
    }
}
