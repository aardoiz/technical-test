# DOCKER - config

SHELL := /usr/bin/env bash
VERSION := latest
IMAGE := "pubmed-chat-api"
SSH_PRIVATE_KEY_FILE=~/.ssh/id_ed25519
SSH_PRIVATE_KEY=$$(cat $(SSH_PRIVATE_KEY_FILE))
BASE_COMMAND := docker compose
CONTAINER_UID=$$(id -u)
CONTAINER_GID=$$(id -g)

check-style:
	poetry run black --config pyproject.toml --diff --check ./
	poetry run darglint -v 2 **/*.py
	poetry run isort --settings-path pyproject.toml --check-only **/*.py
	poetry run mypy --config-file setup.cfg python-template tests/**/*.py

codestyle:
	poetry run isort --settings-path pyproject.toml src apps
	poetry run black --config pyproject.toml ./

test:
	ENV=test poetry run python -m pytest -s

# PYTHON
api:
	ENV=pro poetry run uvicorn apps.chat.http.app:app --host 0.0.0.0 --port 8056

clean-docker:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)

# DOCKER-COMPOSE

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

logs:
	@echo Seeing logs...
	$(BASE_COMMAND) logs

# DOCS
mkdocs:
	poetry run mkdocs serve

ruff:
	poetry run ruff check . --fix --exit-non-zero-on-fix

linters:
	pre-commit run --all-files --color always
