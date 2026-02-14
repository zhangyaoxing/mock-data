# Contributing to MockData

Thank you for your interest in contributing to MockData! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/mockdata.git
   cd mockdata
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/my-new-feature
   ```

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Verify installation**:
   ```bash
   python -m mockdata --help
   pytest
   ```

## Code Standards

### Code Style

We follow PEP 8 and use the following tools:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run all checks before committing:

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Lint
flake8 src tests

# Type check
mypy src
```

### Documentation

- Add docstrings to all public modules, classes, and functions
- Use Google-style docstrings
- Update README.md if adding new features
- Add examples for new functionality

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Run tests before submitting PR:

```bash
pytest
pytest --cov=mockdata --cov-report=html
```

## Pull Request Process

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG** in README.md
5. **Submit PR** with clear description of changes

### PR Title Format

- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update documentation`
- `test: Add tests for feature`
- `refactor: Refactor component`
- `chore: Update dependencies`

## Reporting Issues

When reporting issues, please include:

- Python version
- MockData version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

## Feature Requests

We welcome feature requests! Please:

- Check if feature already exists
- Provide clear use case
- Describe expected behavior
- Consider submitting a PR

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Questions?

Feel free to open an issue for questions or discussion.

Thank you for contributing! 🎉
