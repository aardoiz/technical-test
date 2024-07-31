SHELL := /usr/bin/env bash
VERSION := latest
IMAGE := "aardoiz-chat"
BASE_COMMAND := docker compose
CONTAINER_UID=$$(id -u)
CONTAINER_GID=$$(id -g)

style:
	pre-commit run --all-files

api:
	ENV=pro poetry run uvicorn apps.chat.http.app:app --host 0.0.0.0 --port 8056


build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	$(BASE_COMMAND) up -d --build

up:
	@echo Starting containers...
	$(BASE_COMMAND) up -d

down:
	@echo Stopping and removing all containers, networks and volumes
	$(BASE_COMMAND) down -v

up--db:
	 $(BASE_COMMAND) up mongo -d

down--db:
	 $(BASE_COMMAND) down mongo

up--backend:
	 $(BASE_COMMAND) up backend -d --build

down--backend:
	 $(BASE_COMMAND) down backend

up--qdrant:
	 $(BASE_COMMAND) up qdrant -d

down--qdrant:
	 $(BASE_COMMAND) down qdrant

logs:
	@echo Seeing logs...
	$(BASE_COMMAND) logs
