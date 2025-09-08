# Contributing to Shopify Bulk Importer

Thank you for your interest in contributing to the Shopify Bulk Importer project! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Commit Guidelines](#commit-guidelines)
8. [Pull Request Process](#pull-request-process)
9. [Documentation](#documentation)
10. [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to providing a friendly, safe, and welcoming environment for all contributors, regardless of experience level, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, nationality, or other similar characteristics.

### Expected Behavior

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Publishing others' private information
- Other conduct that could reasonably be considered inappropriate

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up the development environment** (see below)
4. **Create a feature branch** for your changes
5. **Make your changes** following our guidelines
6. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv, virtualenv, or conda)
- Shopify Partner account (for testing)

### Setup Steps

1. Clone your fork:
```bash
git clone https://github.com/yourusername/shopify-bulk-importer.git
cd shopify-bulk-importer
```

2. Add upstream remote:
```bash
git remote add upstream https://github.com/original/shopify-bulk-importer.git
```

3. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

5. Set up pre-commit hooks:
```bash
pre-commit install
```

6. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your test store credentials
```

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template**
3. **Include**:
   - Clear bug description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details

### Suggesting Features

1. **Check existing feature requests**
2. **Use the feature request template**
3. **Include**:
   - Use case description
   - Proposed solution
   - Alternative solutions considered
   - Mockups/examples if applicable

### Code Contributions

1. **Find an issue** labeled "good first issue" or "help wanted"
2. **Comment on the issue** to claim it
3. **Fork and create a branch**:
```bash
git checkout -b feature/your-feature-name
```

4. **Make your changes**
5. **Write/update tests**
6. **Update documentation**
7. **Submit a pull request**

## Coding Standards

### Python Style Guide

We follow PEP 8 with these specific guidelines:

1. **Formatting**:
   - Use Black for code formatting
   - Line length: 88 characters
   - Use type hints for function parameters and returns

2. **Naming Conventions**:
   - Classes: `PascalCase`
   - Functions/Variables: `snake_case`
   - Constants: `UPPER_SNAKE_CASE`
   - Private methods: `_leading_underscore`

3. **Imports**:
   - Standard library first
   - Third-party packages second
   - Local imports last
   - Alphabetical within groups

Example:
```python
import json
import os
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel

from models.smartphone import SmartphoneProduct
from services.shopify_api import ShopifyAPI
```

### Code Structure

1. **File Organization**:
   - One class per file (generally)
   - Related functions in modules
   - Clear separation of concerns

2. **Function Guidelines**:
   - Single responsibility principle
   - Maximum 20 lines (prefer smaller)
   - Clear, descriptive names
   - Docstrings for all public functions

3. **Error Handling**:
   - Use specific exceptions
   - Always include error context
   - Log errors appropriately

Example:
```python
def create_product(self, product_data: dict) -> dict:
    """
    Create a product in Shopify.
    
    Args:
        product_data: Dictionary containing product information
        
    Returns:
        Dictionary with product creation result
        
    Raises:
        ShopifyAPIError: If API call fails
        ValidationError: If product data is invalid
    """
    try:
        # Implementation
        pass
    except requests.RequestException as e:
        raise ShopifyAPIError(f"Failed to create product: {str(e)}")
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests with external services
├── e2e/           # End-to-end workflow tests
└── fixtures/      # Test data and mocks
```

### Writing Tests

1. **Test Naming**:
   - `test_<function_name>_<scenario>_<expected_result>`
   - Example: `test_create_product_valid_data_returns_product_id`

2. **Test Organization**:
   - Arrange, Act, Assert pattern
   - One assertion per test (when possible)
   - Use fixtures for common setup

3. **Coverage Requirements**:
   - Minimum 80% code coverage
   - 100% coverage for critical paths
   - Test edge cases and error scenarios

Example:
```python
import pytest
from services.product_service import ProductService

class TestProductService:
    @pytest.fixture
    def product_service(self):
        return ProductService()
    
    def test_create_smartphone_valid_data_returns_product(self, product_service):
        # Arrange
        smartphone_data = {
            "title": "iPhone 15",
            "brand": "Apple",
            "price": 150000
        }
        
        # Act
        result = product_service.create_smartphone_product(smartphone_data)
        
        # Assert
        assert result["success"] is True
        assert "product_id" in result
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/unit/test_product_service.py

# Run with verbose output
pytest -v
```

## Commit Guidelines

We follow Conventional Commits specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
feat(api): add GraphQL support for product creation

- Implement productSet mutation
- Add GraphQL client configuration
- Update product service to use GraphQL

Closes #123
```

```bash
fix(validation): correct price validation for JPY currency

Price validation was rejecting valid JPY amounts.
Updated to handle non-decimal currencies correctly.
```

### Commit Best Practices

1. Keep commits atomic and focused
2. Write clear, descriptive messages
3. Reference issues in commits
4. Avoid commits like "fix", "update", "WIP"

## Pull Request Process

### Before Submitting

1. **Update your branch**:
```bash
git fetch upstream
git rebase upstream/main
```

2. **Run tests**:
```bash
pytest
black .
flake8
```

3. **Update documentation** if needed

4. **Check your changes**:
```bash
git diff upstream/main
```

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated existing tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by at least one maintainer
3. **Address feedback** promptly
4. **Squash commits** if requested
5. **Merge** when approved

## Documentation

### Documentation Requirements

1. **Code Documentation**:
   - Docstrings for all public APIs
   - Inline comments for complex logic
   - Type hints for clarity

2. **User Documentation**:
   - Update README for new features
   - Add guides for complex workflows
   - Include examples

3. **API Documentation**:
   - Update API_REFERENCE.md
   - Include request/response examples
   - Document error cases

### Documentation Style

```python
def calculate_handle(brand: str, model: str, date: str) -> str:
    """
    Generate a unique product handle.
    
    Creates a handle using brand, model, and date with a daily counter.
    Format: {brand}-{model}-{date}-{counter}
    
    Args:
        brand: Product brand name
        model: Product model name
        date: Date in YYMMDD format
        
    Returns:
        Unique product handle string
        
    Example:
        >>> calculate_handle("apple", "iphone-15", "250730")
        "apple-iphone-15-250730-001"
    """
```

## Community

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Email**: dev@mybyteinternational.com

### Staying Updated

- Watch the repository for updates
- Subscribe to release notifications
- Join our developer newsletter

### Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Annual contributor report

## Additional Resources

- [Architecture Guide](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
- [Testing Guide](docs/testing.md)
- [Shopify API Documentation](https://shopify.dev)

Thank you for contributing to Shopify Bulk Importer! Your efforts help make this tool better for everyone.