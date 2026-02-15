.PHONY: help install install-dev test coverage lint format clean run build

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest

coverage:  ## Run tests with coverage report
	pytest --cov=mockdata --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

lint:  ## Run code quality checks
	flake8 src tests
	pylint src
	mypy src

format:  ## Format code with black and isort
	black src tests
	isort src tests

format-check:  ## Check code formatting without making changes
	black --check src tests
	isort --check-only src tests

clean:  ## Clean up generated files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:  ## Run mockdata generator
	python -m mockdata

build:  ## Build distribution packages
	python -m build

upload-test:  ## Upload to TestPyPI
	python -m twine upload --repository testpypi dist/*

upload:  ## Upload to PyPI
	python -m twine upload dist/*

dev-setup:  ## Initial development setup
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  (Linux/Mac)"
	@echo "  venv\\Scripts\\activate     (Windows)"
	@echo "Then run: make install-dev"

.DEFAULT_GOAL := help
