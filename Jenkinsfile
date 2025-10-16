pipeline {
    agent any

    environment {
        // Define workspace-relative paths for both Windows & Linux
        IS_WINDOWS = "${isUnix() ? 'false' : 'true'}"
        VENV_WIN = "${WORKSPACE}\\venv"
        VENV_LINUX = "${WORKSPACE}/venv"
    }

    triggers {
        // Auto-trigger when a push is made to GitHub
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
                script {
                    if (isUnix()) {
                        echo "🐧 Setting up Python virtual environment (Linux)..."
                        sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        '''
                    } else {
                        echo "🪟 Setting up Python virtual environment (Windows)..."
                        bat """
                        python -m venv "%VENV_WIN%"
                        call "%VENV_WIN%\\Scripts\\activate"
                        "%VENV_WIN%\\Scripts\\pip.exe" install --upgrade pip
                        "%VENV_WIN%\\Scripts\\pip.exe" install -r requirements.txt
                        """
                    }
                }
            }
        }

        stage('Install FIO') {
            steps {
                script {
                    if (isUnix()) {
                        echo "🐧 Installing FIO (Linux)..."
                        sh '''
                        if ! command -v fio &> /dev/null; then
                            sudo apt-get update
                            sudo apt-get install -y fio
                        fi
                        fio --version
                        '''
                    } else {
                        echo "🪟 Checking FIO installation (Windows)..."
                        bat """
                        where fio || choco install fio -y
                        fio --version
                        """
                    }
                }
            }
        }

        stage('Run FIO Tests via Pytest') {
            steps {
                script {
                    if (isUnix()) {
                        echo "🚀 Running FIO tests using Pytest (Linux)..."
                        sh '''
                        . venv/bin/activate
                        mkdir -p results
                        python -m pytest -v --maxfail=1 --disable-warnings \
                            --junitxml=results/report.xml \
                            --html=results/report.html --self-contained-html
                        '''
                    } else {
                        echo "🚀 Running FIO tests using Pytest (Windows)..."
                        bat """
                        call "%VENV_WIN%\\Scripts\\activate"
                        if not exist results mkdir results
                        "%VENV_WIN%\\Scripts\\python.exe" -m pytest -v --maxfail=1 --disable-warnings ^
                            --junitxml=results\\report.xml ^
                            --html=results\\report.html --self-contained-html
                        """
                    }
                }
            }
        }

        stage('Archive & Publish Results') {
            steps {
                echo "📦 Archiving test results and publishing reports..."
                junit 'results/**/*.xml'
                archiveArtifacts artifacts: 'results/**', fingerprint: true

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
            echo "✅ All FIO tests completed successfully!"
        }
        failure {
            echo "❌ Some tests failed — check the 'FIO Test Report' and console output."
        }
        always {
            echo "🧹 Cleaning workspace..."
            deleteDir()
        }
    }
}
