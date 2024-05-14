pipeline {
    agent any
    stages {
        stage('Build Docker Images') {
            steps {
                sh 'cd test_data && docker build -t test_data .'
                sh 'cd model && docker build -t model .'
                sh 'cd test_model && docker build -t test_model .'
                sh 'cd app && docker build -t app .'
            }
        }
        stage('Run Data Tests') {
            steps {
                script {
                    def testResult = sh(
                        script: 'docker run -v /data:/data test_data pytest --verbose',
                        returnStdout: true
                    ).trim()
                    if (testResult.contains("FAILED")) {
                        error("Data tests failed")
                    }
                }
            }
        }
        stage('Train The Model') {
            steps {
                sh 'docker run -v /data:/data -v /models:/models --gpus all model'
            }
        }
        stage('Run Model Tests') {
            steps {
                script {
                    def testResult = sh(
                        script: 'docker run -v /data:/data -v /models:/models test_model pytest --verbose',
                        returnStdout: true
                    ).trim()
                    if (testResult.contains("FAILED")) {
                        error("Model tests failed")
                    }
                }
            }
        }
        stage('Start Streamlit App') {
            steps {
                sh 'docker run -d -v /models:/app/models/ -p 8501:8501 app'
            }
        }
    }
}