.PHONY: init help build-api build-bot down up logs-api logs-bot build fast

include .env
export $(shell sed 's/=.*//' .env)

default: build

help:
	@echo "Help: "
	@echo "init: Recussive update submodules"
	@echo "up: Docker compose up"
	@echo "down: Docker compose down"
	@echo "build: Build all containers without cache"
	@echo "logs: APP logs bottom 1000 and -f"
	@echo "logs-nginx: Nginx logs bottom 1000 and -f"

init:
	git submodule update --init --recursive

bash:
	docker-compose exec emp-portal bash

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build
	docker-compose up -d

build-nocache:
	docker-compose build --no-cache
	docker-compose up -d

logs:
	docker-compose logs -f --tail=1000 emp-portal 

migrations:


migrate:


delete-migrations:

	
