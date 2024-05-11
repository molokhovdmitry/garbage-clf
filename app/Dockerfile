FROM pytorch/pytorch:latest

USER root

WORKDIR /app/app
COPY . /app/app

# Install the requirements
RUN pip3 install --upgrade pip && \
    pip3 install -Ur requirements.txt

EXPOSE 8501

# Run streamlit
CMD [ "streamlit", "run", "app.py", "--server.address=0.0.0.0" ]
