# Makefile for Docker Compose tasks

# Set the default shell to bash
SHELL := /bin/bash
PYTEST = pytest
CONTAINER_NAME = transmitata-web-1

# Install dependencies and set up pre-commit hooks
setup:
	pip install -r requirements.txt
	pre-commit install

# Target to bring up the Docker Compose services
start:
	@echo "Starting Docker Compose services..."
	docker compose up

# Target to execute a bash shell in the running web container
shell:
	@echo "Executing bash in the $(CONTAINER_NAME) container..."
	docker exec -it $(CONTAINER_NAME) bash

# Target to run Django tests
tests:
	@echo "Running Django tests..."
	python3 manage.py test api.tests web.tests

# Lint with ruff
lint:
	ruff check .

# Format with ruff
format:
	ruff format .

# Check formatting without applying changes
format-check:
	ruff format --check .

# Help message
help:
	@echo "Makefile commands:"
	@echo "  setup           - Install dependencies and pre-commit hooks"
	@echo "  start           - Start docker compose"
	@echo "  shell           - Run bash inside the container"
	@echo "  tests           - Run Django tests (api and web apps)"
	@echo "  lint            - Run ruff linter"
	@echo "  format          - Format code with ruff"
	@echo "  format-check    - Check formatting without changes"

.PHONY: setup start shell tests lint format format-check help
