# Makefile for Docker Compose tasks

# Set the default shell to bash
SHELL := /bin/bash
PYTEST = pytest
CONTAINER_NAME = transmitata-web-1

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

# Help message
help:
	@echo "Makefile commands:"
	@echo "  start           - Start docker compose"
	@echo "  shell           - Run bash inside the container"
	@echo "  tests           - Run Django tests (api and web apps)"

.PHONY: start start-detached shell down test coverage help
