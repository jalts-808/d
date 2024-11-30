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
        stage('Seed Database') {
            steps {
                echo 'Starting Seed Database Stage...'
                sh 'pwd'
                sh 'ls -R'
                sh '''
                    . venv/bin/activate
                    export PYTHONPATH=$PYTHONPATH:$WORKSPACE/ecom
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
            echo 'Starting Debugging Stage at the End...'
            sh 'echo "Final PATH: $PATH"'
            sh 'python3 --version || python --version'
            sh 'python3 -m pip --version || python -m pip --version'
            sh 'env'
            sh 'echo PYTHONPATH: $PYTHONPATH'
            echo 'Publishing test results...'
            script {
                def testFiles = findFiles(glob: 'pytest_report.xml')
                if (testFiles.length > 0) {
                    junit 'pytest_report.xml'
                } else {
                    echo 'No test report found. Skipping JUnit reporting.'
                }
            }
        }
    }
}
