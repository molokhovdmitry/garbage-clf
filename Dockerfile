FROM jenkins/jenkins:lts

# Install Python and pip
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


# Install requirements
RUN pip install --upgrade pip && \
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip3 install kaggle scikit-learn pandas numpy

USER jenkins
