# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY *.py ./

RUN pip3 install -r requirements.txt

EXPOSE 8000
EXPOSE 3306

CMD [ "python3", "server.py", "--host=0.0.0.0"]
