FROM python:3.12.3-slim

ENV APP_HOME /app

RUN apt-get update && apt-get install -y git && apt-get clean

RUN pip install --upgrade pip

WORKDIR $APP_HOME

COPY . ./

RUN pip install -r requirements.txt

CMD python3 main.py
