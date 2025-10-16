pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}/venv"
        PYTHON = "${WORKSPACE}/venv/bin/python"
        PIP = "${WORKSPACE}/venv/bin/pip"
    }

    triggers {
        githubPush() // Trigger Jenkins pipeline automatically on GitHub push
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV}
                ${PIP} install --upgrade pip
                ${PIP} install -r requirements.txt
                '''
            }
        }

        stage('Run FIO Tests via Pytest') {
            steps {
                sh '''
                ${PYTHON} -m pytest -v --maxfail=1 --disable-warnings --junitxml=results/report.xml
                '''
            }
        }

        stage('Archive Test Results') {
            steps {
                junit 'results/report.xml'
                archiveArtifacts artifacts: 'results/**', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace..."
            deleteDir()
        }
    }
}
