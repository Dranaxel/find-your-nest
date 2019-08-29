FROM python:3.7-buster

RUN apt-get update \
    && apt-get install -y libpq-dev
    
RUN pip3 install pipenv

COPY . /app

WORKDIR /app
RUN pipenv install

EXPOSE 5000


CMD pipenv run python3 main.py
