NAME=$(shell basename "$$(pwd)")

all:build run

build:
~   docker build -t $(NAME) . 

run:
~   docker run -it

test: build
~   docker run fynbea pipenv run pytest

deliver:
~   docker tag $(NAME) $(NAME):20190829
~   docker push $(NAME)  
