pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Starting Checkout Stage...'
                checkout scm
                sh 'pwd' // Print current working directory
                sh 'ls -la' // List files for debugging
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Starting Install Dependencies Stage...'
                sh 'python3 --version || python --version' // Ensure Python is available
                sh 'python3 -m pip --version || python -m pip --version' // Ensure pip is available
                sh 'python3 -m venv venv || python -m venv venv' // Create virtual environment
                sh '''
                    source venv/bin/activate || . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                ''' // Activate venv and install dependencies
            }
        }
        stage('Seed Database') {
            steps {
                echo 'Starting Seed Database Stage...'
                sh 'pwd' // Print current working directory
                sh 'ls -la' // List files for debugging
                sh '''
                    source venv/bin/activate || . venv/bin/activate
                    python scripts/seed_db.py
                ''' // Seed database
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Starting Run Tests Stage...'
                sh 'pwd' // Print current working directory
                sh 'ls -la' // List files for debugging
                sh '''
                    source venv/bin/activate || . venv/bin/activate
                    pytest --junitxml=pytest_report.xml --maxfail=5 --disable-warnings
                ''' // Run tests
                sh 'ls -la pytest_report.xml' // Verify pytest report exists
            }
        }
    }
    post {
        always {
            echo 'Publishing test results...'
            junit 'pytest_report.xml' // Publish the test results
        }
    }
}
