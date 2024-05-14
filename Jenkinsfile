pipeline {
    agent any
    stages {
        stage('Run Data Tests') {
            steps {
                sh 'cd test_data && docker build -t test_data .'
                sh 'docker run -v /home/nomad/projects/garbage-clf/data:/data test_data pytest --verbose'
            }
        }
        stage('Train The Model') {
            steps {
                sh 'cd model && docker build -t model .'
                sh 'docker run -v /home/nomad/projects/garbage-clf/data:/data -v /home/nomad/projects/garbage-clf/models:/models --gpus all model'
            }
        }
        stage('Run Model Tests') {
            steps {
                script {
                    sh 'cd test_model && docker build -t test_model .'
                    def testResult = sh(
                        script: 'docker run -v /home/nomad/projects/garbage-clf/data:/data -v /home/nomad/projects/garbage-clf/models:/models test_model pytest --verbose',
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
                sh 'cd app && docker build -t app .'
                sh 'docker run -d -v /home/nomad/projects/garbage-clf/models:/app/models/ -p 8501:8501 app'
            }
        }
    }
}
