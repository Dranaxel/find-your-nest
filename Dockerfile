FROM python:3.5

RUN apt-get update \
    && apt-get install -y libpq-dev
    
RUN pip3 install pipenv

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

EXPOSE 8080
RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
