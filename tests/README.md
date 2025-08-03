# Test Suite Documentation

This directory contains the comprehensive test suite for the Shopify Bulk Importer project.

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── requirements.txt         # Test-specific dependencies
├── README.md               # This file
├── unit/                   # Unit tests (fast, isolated)
│   ├── models/            # Model validation tests
│   ├── services/          # Service logic tests
│   ├── config/           # Configuration tests
│   └── utils/            # Utility function tests
├── integration/           # Integration tests (with external dependencies)
│   ├── api/              # Shopify API integration tests
│   ├── workflows/        # Cross-component workflow tests
│   └── repositories/     # Repository implementation tests
├── e2e/                  # End-to-end tests (full system)
│   ├── smartphone_workflow.py
│   ├── laptop_workflow.py
│   └── ui_interactions.py
├── performance/          # Performance and load tests
│   ├── benchmarks/       # Performance benchmarks
│   └── load_tests/       # Load testing scenarios
└── fixtures/             # Test data and mock responses
    ├── shopify_responses/
    ├── test_data.json
    └── mock_products.py
```

## Test Categories

### Unit Tests (`unit/`)
- **Purpose**: Test individual functions and methods in isolation
- **Speed**: Fast (< 1s per test)
- **Dependencies**: None (fully mocked)
- **Coverage Target**: >90% for critical business logic

### Integration Tests (`integration/`)
- **Purpose**: Test component interactions and API integrations
- **Speed**: Medium (1-10s per test)
- **Dependencies**: May use test API endpoints or databases
- **Coverage Target**: >80% for critical workflows

### End-to-End Tests (`e2e/`)
- **Purpose**: Test complete user workflows through the UI
- **Speed**: Slow (10s+ per test)
- **Dependencies**: Full system required
- **Coverage Target**: Critical user paths covered

### Performance Tests (`performance/`)
- **Purpose**: Validate performance and resource usage
- **Speed**: Variable
- **Dependencies**: Production-like data sets
- **Coverage Target**: All performance-critical operations

## Running Tests

### Quick Test Run
```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest -m unit          # Unit tests only
python -m pytest -m integration   # Integration tests only
python -m pytest -m e2e          # E2E tests only
```

### Test with Coverage
```bash
# Generate coverage report
python -m pytest --cov=. --cov-report=html --cov-report=term

# View coverage in browser
open htmlcov/index.html
```

### Parallel Test Execution
```bash
# Run tests in parallel (faster execution)
python -m pytest -n auto
```

### Performance Testing
```bash
# Run performance benchmarks
python -m pytest performance/ --benchmark-only
```

## Test Configuration

### Environment Setup
Tests automatically use test environment variables defined in `conftest.py`:
- `SHOPIFY_ACCESS_TOKEN=test_access_token`
- `SHOPIFY_API_KEY=test_api_key`
- `SHOPIFY_API_SECRET=test_api_secret`
- `SHOPIFY_SHOP_DOMAIN=test-shop.myshopify.com`

### Markers
Tests are automatically marked based on their location:
- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.e2e`: End-to-end tests
- `@pytest.mark.api`: Tests that interact with Shopify API
- `@pytest.mark.slow`: Slow-running tests

### Fixtures
Common fixtures available in all tests:
- `test_config`: Test configuration dictionary
- `mock_shopify_api`: Mocked Shopify API client
- `sample_smartphone_data`: Sample smartphone test data
- `sample_laptop_data`: Sample laptop test data
- `mock_dependency_container`: Mocked DI container

## Writing Tests

### Unit Test Example
```python
import pytest
from services.product_service import ProductService

class TestProductService:
    def test_create_product_title(self, sample_smartphone_data):
        service = ProductService()
        title = service.generate_title(sample_smartphone_data)
        assert "iPhone 14 Pro" in title
        assert "128GB" in title
```

### Integration Test Example
```python
import pytest

@pytest.mark.integration
class TestShopifyIntegration:
    def test_product_creation_workflow(self, mock_shopify_api, sample_smartphone_data):
        # Test complete product creation workflow
        pass
```

### Performance Test Example
```python
import pytest

@pytest.mark.performance
def test_product_creation_performance(benchmark, sample_smartphone_data):
    result = benchmark(create_product, sample_smartphone_data)
    assert result is not None
```

## Coverage Requirements

### Minimum Coverage Targets
- **Critical Business Logic**: 95%
- **API Integration**: 90%
- **User Workflows**: 85%
- **Utility Functions**: 80%
- **Overall Project**: 80%

### Coverage Exclusions
- Third-party libraries
- Configuration files
- Test files themselves
- Development utilities

## Continuous Integration

### GitHub Actions Integration
Tests run automatically on:
- Pull requests
- Pushes to main branch
- Nightly builds

### Test Pipeline Stages
1. **Linting**: Code style and quality checks
2. **Unit Tests**: Fast, isolated tests
3. **Integration Tests**: Component interaction tests
4. **Coverage Analysis**: Coverage report generation
5. **Performance Tests**: Benchmark validation

## Test Data Management

### Fixtures and Mock Data
- Use `fixtures/` for static test data
- Use factories for dynamic test data generation
- Mock external API responses consistently

### Test Database
- Use in-memory databases for unit tests
- Use test databases for integration tests
- Reset state between tests automatically

## Debugging Tests

### Running Single Tests
```bash
# Run specific test file
python -m pytest tests/unit/services/test_product_service.py

# Run specific test method
python -m pytest tests/unit/services/test_product_service.py::TestProductService::test_create_title
```

### Verbose Output
```bash
# Detailed test output
python -m pytest -v --tb=long

# Stop on first failure
python -m pytest -x
```

### Test Debugging
```python
# Add breakpoints in tests
import pdb; pdb.set_trace()

# Use pytest debugging
pytest --pdb
```

## Best Practices

### Test Organization
- One test file per source file
- Group related tests in test classes
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### Test Quality
- Test behavior, not implementation
- Use meaningful assertions
- Avoid testing third-party libraries
- Keep tests independent and isolated

### Performance
- Keep unit tests under 1 second
- Use mocks for external dependencies
- Run slow tests separately
- Optimize test data setup

## Maintenance

### Regular Tasks
- Review and update test coverage
- Remove obsolete tests
- Update mock data to match API changes
- Optimize slow-running tests

### Test Health Monitoring
- Monitor test execution times
- Track test failure rates
- Ensure consistent test environments
- Regular dependency updates