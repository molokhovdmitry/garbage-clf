FROM pytorch/torchserve:0.10.0-cpu

USER root

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "pytest" ]
