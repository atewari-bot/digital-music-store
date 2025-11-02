# Makefile for Digital Music Store Project
# Variables
PYTHON := python3
PIP := pip3
VENV := .venv
VENV_BIN := $(VENV)/bin
PYTHON_EXECUTABLE := $(VENV_BIN)/python
PIP_VENV := $(VENV_BIN)/pip

# Project Strucuture
SRC_DIR := src
TESTS_DIR := tests

# Default target
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "}; NF==2 {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: venv
venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP_VENV) install --upgrade pip setuptools wheel

.PHONY: venv-clean
venv-clean:
	@echo "Cleaning virtual environment..."
	@rm -rf $(VENV)

.PHONY: install
install: venv
	@echo "Installing dependencies..."
	@$(PIP_VENV) install --upgrade pip
	@$(PIP_VENV) install -r requirements.txt

.PHONY: test
test:
	@echo "Running tests..."
	$(PYTHON_EXECUTABLE) tests/tests.py

.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__ $(SRC_DIR)/__pycache__ $(TESTS_DIR)/__pycache__

.PHONY: lint
lint:
	@echo "Running linters..."
	$(VENV_BIN)/flake8 src tests
	$(VENV_BIN)/pylint src tests

.PHONY: run
run:
	@echo "Running the application..."
	$(PYTHON_EXECUTABLE) -c "from utils.env import load_environment_variables; load_environment_variables()"
	$(PYTHON_EXECUTABLE) -m src.main

.PHONY: docker-build
docker-build:
	@echo "Building Docker images..."
	docker-compose build

.PHONY: docker-up
docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d

.PHONY: docker-down
docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

.PHONY: docker-logs
docker-logs:
	@echo "Viewing Docker logs..."
	docker-compose logs -f

.PHONY: docker-dev
docker-dev:
	@echo "Starting Docker containers in development mode..."
	docker-compose -f docker-compose.dev.yml up --build

.PHONY: docker-clean
docker-clean:
	@echo "Cleaning up Docker containers and volumes..."
	docker-compose down -v
	docker system prune -f