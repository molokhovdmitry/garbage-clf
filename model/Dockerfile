FROM pytorch/pytorch:latest

USER root

WORKDIR /app
COPY . /app

# Install the requirements
RUN pip3 install --upgrade pip && \
    pip3 install -Ur requirements.txt

# Run the pipeline
CMD ["python", "train_model.py"]
