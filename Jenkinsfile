pipeline {
    agent any
    stages {
        stage('Run Data Tests') {
            steps {
                sh 'cd test_data && docker build -t test_data .'
                sh 'docker run --rm \
                    --env-file $PROJECT_DIR/.env \
                    -v $PROJECT_DIR/data:/data \
                    test_data'
            }
        }
        stage('Train The Model') {
            steps {
                sh 'cd model && docker build -t model .'
                sh 'docker run --rm \
                    --env-file $PROJECT_DIR/.env \
                    -v $PROJECT_DIR/data:/data \
                    -v $PROJECT_DIR/models:/models \
                    --gpus all model'
            }
        }
        stage('Run Model Tests') {
            steps {
                sh 'cd test_model && docker build -t test_model .'
                sh 'docker run --rm \
                    --env-file $PROJECT_DIR/.env \
                    -v $PROJECT_DIR/data:/data \
                    -v $PROJECT_DIR/models:/models \
                    test_model'
            }
        }
        stage('Start Streamlit App') {
            steps {
                sh 'cd app && docker build -t app .'
                sh 'docker run -d --rm \
                    --env-file $PROJECT_DIR/.env \
                    -v $PROJECT_DIR/models:/app/models/ \
                    -p 8501:8501 \
                    app'
            }
        }
    }
}
