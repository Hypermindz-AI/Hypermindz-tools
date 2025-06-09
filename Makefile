.PHONY: help install install-dev test lint format type-check clean build upload docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install the package"
	@echo "  install-dev  Install in development mode with dev dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black"
	@echo "  type-check   Run type checking with mypy"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build distribution packages"
	@echo "  upload       Upload to PyPI (requires credentials)"
	@echo "  docs         Generate documentation"
	@echo "  check-all    Run all checks (lint, type-check, test)"

install:
	pip install .

install-dev:
	pip install -e .[dev]

test:
	pytest tests/ -v --cov=hypermindz_tools --cov-report=term-missing

test-verbose:
	pytest tests/ -v -s --cov=hypermindz_tools --cov-report=html

lint:
	flake8 hypermindz_tools tests
	black --check hypermindz_tools tests

format:
	black hypermindz_tools tests examples

type-check:
	mypy hypermindz_tools --ignore-missing-imports

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	twine check dist/*
	twine upload dist/*

upload-test: build
	twine check dist/*
	twine upload --repository testpypi dist/*

check-all: lint type-check test
	@echo "All checks passed!"

# Development setup
setup-dev: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make check-all' to verify everything works."

# Quick development cycle
dev-cycle: format lint type-check test
	@echo "Development cycle complete!"