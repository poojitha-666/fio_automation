pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}\\venv"
        PYTHON = "${WORKSPACE}\\venv\\Scripts\\python.exe"
        PIP = "${WORKSPACE}\\venv\\Scripts\\pip.exe"
    }

    triggers {
        // Trigger pipeline automatically when GitHub push happens
        githubPush()
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out code from GitHub..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "Setting up Python virtual environment..."
                bat """
                python -m venv "%VENV%"
                call "%VENV%\\Scripts\\activate"
                "%PIP%" install --upgrade pip
                "%PIP%" install -r requirements.txt
                """
            }
        }

        stage('Run FIO Tests via Pytest') {
            steps {
                echo "Running FIO workload tests..."
                bat """
                call "%VENV%\\Scripts\\activate"
                "%PYTHON%" -m pytest -v --maxfail=1 --disable-warnings --junitxml=results\\report.xml
                """
            }
        }

        stage('Archive Results') {
            steps {
                echo "Archiving test results..."
                junit 'results\\report.xml'
                archiveArtifacts artifacts: 'results\\**', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ All FIO tests completed successfully."
        }
        failure {
            echo "❌ Some tests failed — check the logs in Jenkins results tab."
        }
        always {
            echo "Cleaning workspace..."
            deleteDir()
        }
    }
}
