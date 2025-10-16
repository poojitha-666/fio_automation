pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}\\venv"
        PYTHON = "${WORKSPACE}\\venv\\Scripts\\python.exe"
        PIP = "${WORKSPACE}\\venv\\Scripts\\pip.exe"
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "📥 Checking out code from GitHub..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "🪟 Setting up Python virtual environment..."
                bat """
                python -m venv "%VENV%"
                call "%VENV%\\Scripts\\activate"
                "%PYTHON%" -m pip install --upgrade pip
                "%PIP%" install -r requirements.txt || echo "⚠️ requirements.txt not found, installing manually..."
                "%PIP%" install pytest pytest-html
                "%PIP%" list
                """
            }
        }

        stage('Install FIO') {
            steps {
                echo "🪟 Checking FIO installation..."
                bat """
                where fio || choco install fio -y
                fio --version
                """
            }
        }

        stage('Run FIO Tests via Pytest') {
            steps {
                echo "🚀 Running FIO workload tests..."
                bat """
                call "%VENV%\\Scripts\\activate"
                if not exist results mkdir results
                "%PYTHON%" -m pytest -v --maxfail=1 --disable-warnings ^
                    --junitxml=results\\report.xml ^
                    --html=results\\report.html --self-contained-html
                """
            }
        }

        stage('Archive & Publish Results') {
            steps {
                echo "📦 Archiving and publishing results..."
                junit 'results\\report.xml'
                archiveArtifacts artifacts: 'results\\**', fingerprint: true

                publishHTML(target: [
                    reportDir: 'results',
                    reportFiles: 'report.html',
                    reportName: 'FIO Test Report',
                    alwaysLinkToLastBuild: true,
                    keepAll: true
                ])
            }
        }
    }

    post {
        success {
            echo "✅ All FIO tests completed successfully."
        }
        failure {
            echo "❌ Some tests failed — check logs or the FIO Test Report."
        }
        always {
            echo "🧹 Cleaning workspace..."
            deleteDir()
        }
    }
}
