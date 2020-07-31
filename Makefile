.PHONY: init help build-api build-bot down up logs-api logs-bot build fast

include .env
export $(shell sed 's/=.*//' .env)

default: build

help:
	@echo "Help: "
	@echo "init: Recussive update submodules"
	@echo "bash: Go inside emp-portal container"
	@echo "up: Bring all the container up"
	@echo "down: Bring down all the containers"
	@echo "logs: APP logs bottom 1000 and -f"
	@echo "build: Build all the containers (Do not use this for first time, instead  use initial-build)"
	@echo "initial-build: Build all the containers for the first time"
	@echo "logs-webpack: Webpack logs"
	@echo "emp-migrate: Migrate all application, use this only if there are any database changes"
	@echo "superuser: Create superuser"
	@echo "generate-apikey: Generate api key for the user. API key is required to load the initial data."
	@echo "initial-data: Load initial data for testing/dev purpose."
	@echo "index: Rebuild index"

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

initial-build: build emp-migrate

build-nocache:
	docker-compose build --no-cache
	docker-compose up -d

logs:
	docker-compose logs -f --tail=1000 emp-portal 

logs-webpack:
	docker-compose logs -f --tail=100 webpack

migrations:
	docker-compose exec emp-portal python ./app/manage.py makemigrations hr_mgmt project_mgmt task_mgmt

migrate-ext:
	docker-compose exec emp-portal python ./app/manage.py migrate hr_mgmt
	docker-compose exec emp-portal python ./app/manage.py migrate project_mgmt
	docker-compose exec emp-portal python ./app/manage.py migrate task_mgmt

core-migrations:
	docker-compose exec emp-portal python ./app/manage.py makemigrations
	docker-compose exec emp-portal python ./app/manage.py migrate

emp-migrate: migrations migrate-ext core-migrations

superuser:
	docker-compose exec emp-portal python ./app/manage.py createsuperuser

generate-apikey:
	docker-compose exec emp-portal python ./app/manage.py generate_api_key

index:
	docker-compose exec emp-portal python ./app/manage.py search_index --rebuild

initial-data:
	docker-compose up -d
	docker-compose exec emp-portal python ./load_data.py

test-hr_mgmt:
	docker-compose up -d
	docker-compose exec emp-portal python ./app/manage.py test ./extensions/emappext-hr_mgmt/emappext/hr_mgmt/tests/

