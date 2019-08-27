FROM debian:10

RUN apt-get update

RUN apt-get install -y python3 libpq-dev python3-pip

RUN pip3 install flask flask-login opencage passlib

COPY . /app  


EXPOSE 5000

#CMD  main.py
WORKDIR /app

CMD python3 main.py
