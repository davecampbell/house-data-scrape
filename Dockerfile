FROM python:3.8-slim-buster

WORKDIR /app

RUN apt update
RUN apt-get update -y
RUN apt-get install chromium-driver -y

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

#
# EXPOSE 8501

COPY app/ .

RUN mkdir /app/out

CMD python3 /app/app.py
