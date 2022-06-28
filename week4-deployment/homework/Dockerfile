FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN apt-get update -y && apt-get install -y gcc
RUN pipenv install --system --deploy

COPY [ "docker_starter.py", "model.bin", "./" ]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "docker_starter:app" ]