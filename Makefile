.PHONY: help install install-dev test lint format type-check clean build upload docs pre-commit-install pre-commit-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install         Install the package"
	@echo "  install-dev     Install in development mode with dev dependencies"
	@echo "  test            Run tests"
	@echo "  lint            Run linting checks"
	@echo "  format          Format code with black and isort"
	@echo "  type-check      Run type checking with mypy"
	@echo "  clean           Clean build artifacts"
	@echo "  build           Build distribution packages"
	@echo "  upload          Upload to PyPI (requires credentials)"
	@echo "  upload-test     Upload to Test PyPI"
	@echo "  docs            Generate documentation"
	@echo "  check-all       Run all checks (lint, type-check, test)"
	@echo "  pre-commit-install  Install pre-commit hooks"
	@echo "  pre-commit-run      Run pre-commit on all files"
	@echo "  setup-dev       Complete development environment setup"
	@echo "  dev-cycle       Quick development cycle (format, lint, type-check, test)"
	@echo "  fix-all         Auto-fix formatting issues and run all checks"

install:
	python -m pip install .

install-dev:
	python -m pip install -e .[dev]
	python -m pip install pre-commit

test:
	pytest tests/ -v --cov=hypermindz_tools --cov-report=term-missing

test-verbose:
	pytest tests/ -v -s --cov=hypermindz_tools --cov-report=html

lint:
	@echo "Running flake8..."
	flake8 hypermindz_tools tests --max-line-length=127 --max-complexity=10
	@echo "Checking black formatting..."
	black --check --diff hypermindz_tools tests
	@echo "Checking isort..."
	isort --check-only --diff hypermindz_tools tests

format:
	@echo "Formatting with black..."
	black hypermindz_tools tests examples
	@echo "Sorting imports with isort..."
	isort hypermindz_tools tests examples

type-check:
	@echo "Running mypy type checking..."
	mypy hypermindz_tools --ignore-missing-imports

# Security check
security:
	@echo "Running bandit security check..."
	bandit -r hypermindz_tools -f json -o bandit-report.json || true

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf bandit-report.json
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

# Pre-commit related targets
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Pre-commit hooks installed successfully!"

pre-commit-run:
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files

pre-commit-update:
	@echo "Updating pre-commit hooks..."
	pre-commit autoupdate

# Enhanced check targets
check-all: lint type-check security test
	@echo "All checks passed!"

# Auto-fix and verify
fix-all: format lint type-check test
	@echo "Code fixed and all checks passed!"

# Development setup with pre-commit
setup-dev: install-dev pre-commit-install
	@echo "Development environment setup complete!"
	@echo "Pre-commit hooks are now installed."
	@echo "Run 'make check-all' to verify everything works."
	@echo "Run 'make pre-commit-run' to test pre-commit on all files."

# Quick development cycle with auto-formatting
dev-cycle: format lint type-check test
	@echo "Development cycle complete!"

# CI simulation - what CI will run
ci-check: lint type-check security test
	@echo "CI checks simulation complete!"

# Generate documentation
docs:
	@echo "Generating documentation..."
	# Add your documentation generation commands here
	# sphinx-build -b html docs/ docs/_build/

# Display project info
info:
	@echo "Project: Hypermindz Tools"
	@echo "Python version: $$(python --version)"
	@echo "Pip version: $$(pip --version)"
	@echo "Pre-commit version: $$(pre-commit --version 2>/dev/null || echo 'Not installed')"
	@echo "Git hooks installed: $$(test -f .git/hooks/pre-commit && echo 'Yes' || echo 'No')"
