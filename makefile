
POETRY_VERSION := 1.8.5
CLI_NAME := "oss4climate.cli"

.PHONY: install
install:
	pip install pipx
	pipx ensurepath
	pipx install poetry==$(POETRY_VERSION) || echo "Poetry already installed"
	poetry config virtualenvs.create true 
	poetry install --no-cache
	
