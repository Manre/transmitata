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

# Help message
help:
	@echo "Makefile commands:"
	@echo "  start       - Start docker compose"
	@echo "  shell       - Run bash inside the container"

.PHONY: start start-detached shell down test coverage help
