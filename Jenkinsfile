groovy
pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            // Need some extra packages for Selenium in Docker
            args '-u root:root'
        }
    }
    stages {
        stage('Install') {
            steps {
                sh 'apt-get update && apt-get install -y chromium chromium-driver'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test & Coverage') {
            steps {
                sh 'coverage run --branch -m pytest tests/ -v'
                sh 'coverage report -m'
            }
        }
    }
}