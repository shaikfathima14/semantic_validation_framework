pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images...'
                bat 'docker compose build'
            }
        }

        stage('Start Application') {
            steps {
                echo 'Starting application...'
                bat 'docker compose up -d'
            }
        }

        stage('Check Containers') {
            steps {
                echo 'Checking Docker containers...'
                bat 'docker compose ps'
            }
        }

        stage('Application Test') {
            steps {
                echo 'Testing backend health endpoint...'
                bat 'curl -f http://localhost:8000/health'
            }
        }

    }

    post {

        success {
            echo '======================================'
            echo 'SemanticAI deployment successful!'
            echo '======================================'
        }

        failure {
            echo '======================================'
            echo 'Build or deployment failed.'
            echo 'Check the Jenkins console output.'
            echo '======================================'
        }

        always {
            echo 'Jenkins pipeline completed.'
        }
    }
}