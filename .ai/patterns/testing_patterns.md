# Testing Patterns

This document establishes standardized testing patterns for the Shopify Bulk Importer project, ensuring comprehensive test coverage, maintainable test code, and reliable quality assurance.

## Overview

**Purpose**: Standardized testing patterns and best practices
**Scope**: All test types (unit, integration, E2E)
**Maintainer**: Code Quality Architect

## Testing Philosophy

### 1. Test Pyramid
Focus on fast, reliable unit tests with strategic integration and E2E tests.

```
        /\
       /  \
      / E2E \      <- Few, high-value scenarios
     /______\
    /        \
   /Integration\ <- Key component interactions
  /__________\
 /            \
/   Unit Tests  \   <- Majority of tests
/________________\
```

### 2. Testing Principles
- **Fast**: Tests should run quickly to enable frequent execution
- **Independent**: Tests should not depend on each other
- **Repeatable**: Tests should produce consistent results
- **Self-Validating**: Tests should have clear pass/fail criteria
- **Timely**: Tests should be written close to the code they test

## Unit Testing Patterns

### Test Structure Pattern (AAA)
```python
import pytest
from unittest.mock import Mock, patch
from services.product_service import ProductService
from models.smartphone import SmartphoneProduct

class TestProductService:
    """Test ProductService functionality."""
    
    def test_create_smartphone_product_success(self):
        """Test successful smartphone product creation."""
        
        # Arrange
        product_data = {
            "title": "iPhone 15 Pro Max 256GB Space Black",
            "brand": "Apple",
            "model": "iPhone 15 Pro Max",
            "price": 159800
        }
        
        mock_api_client = Mock()
        mock_api_client.create_product.return_value = {
            "id": 123456,
            "title": product_data["title"],
            "handle": "iphone-15-pro-max-256gb-space-black"
        }
        
        service = ProductService(api_client=mock_api_client)
        
        # Act
        result = service.create_smartphone_product(product_data)
        
        # Assert
        assert result["id"] == 123456
        assert result["title"] == product_data["title"]
        mock_api_client.create_product.assert_called_once()
```

### Mock Patterns
```python
# Domain Service Testing with Mocks
class TestProductDomainService:
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock repository."""
        return Mock(spec=ProductRepositoryInterface)
    
    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mocked dependencies."""
        return ProductDomainService(repository=mock_repository)
    
    def test_create_product_validates_required_fields(self, service, mock_repository):
        """Test that service validates required fields."""
        
        # Arrange
        invalid_data = {"title": ""}  # Missing required fields
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.create_product(invalid_data)
        
        assert "title" in str(exc_info.value)
        mock_repository.save.assert_not_called()
    
    def test_create_product_calls_repository(self, service, mock_repository):
        """Test that service calls repository with valid data."""
        
        # Arrange
        valid_data = {
            "title": "Test Product",
            "brand": "Apple",
            "price": 100000
        }
        
        mock_repository.save.return_value = SmartphoneEntity(
            id="123", 
            **valid_data
        )
        
        # Act
        result = service.create_product(valid_data)
        
        # Assert
        assert result.id == "123"
        mock_repository.save.assert_called_once()
```

### Parameterized Testing Pattern
```python
@pytest.mark.parametrize("price,expected_valid", [
    (0, False),        # Zero price invalid
    (-100, False),     # Negative price invalid
    (100, True),       # Positive price valid
    (999999, True),    # Large price valid
])
def test_price_validation(price, expected_valid):
    """Test price validation with various inputs."""
    
    product_data = {
        "title": "Test Product",
        "brand": "Apple",
        "price": price
    }
    
    if expected_valid:
        # Should not raise exception
        product = SmartphoneProduct(**product_data)
        assert product.price == price
    else:
        # Should raise validation error
        with pytest.raises(ValidationError):
            SmartphoneProduct(**product_data)

@pytest.mark.parametrize("brand,model,expected_handle", [
    ("Apple", "iPhone 15", "apple-iphone-15"),
    ("Samsung", "Galaxy S24", "samsung-galaxy-s24"),
    ("Google", "Pixel 8 Pro", "google-pixel-8-pro"),
])
def test_handle_generation(brand, model, expected_handle):
    """Test handle generation for different brands and models."""
    
    service = HandleGenerator()
    result = service.generate_handle(brand, model)
    
    assert expected_handle in result
    assert result.count("-") >= 2  # Contains date and counter
```

### Exception Testing Pattern
```python
class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_api_authentication_error_handling(self):
        """Test handling of API authentication errors."""
        
        # Arrange
        mock_api_client = Mock()
        mock_api_client.create_product.side_effect = AuthenticationError("Invalid token")
        
        service = ProductService(api_client=mock_api_client)
        
        # Act & Assert
        with pytest.raises(ProductCreationError) as exc_info:
            service.create_smartphone_product({"title": "Test"})
        
        assert "authentication" in str(exc_info.value).lower()
    
    def test_rate_limit_error_triggers_retry(self):
        """Test that rate limit errors trigger retry logic."""
        
        # Arrange
        mock_api_client = Mock()
        mock_api_client.create_product.side_effect = [
            RateLimitError("Rate limited", retry_after=1),
            {"id": 123, "title": "Success"}  # Second call succeeds
        ]
        
        service = ProductService(api_client=mock_api_client)
        
        # Act
        result = service.create_smartphone_product({"title": "Test Product"})
        
        # Assert
        assert result["id"] == 123
        assert mock_api_client.create_product.call_count == 2
```

## Integration Testing Patterns

### API Integration Testing
```python
import pytest
import requests_mock
from services.shopify_api import ShopifyAPIClient

class TestShopifyAPIIntegration:
    """Test Shopify API integration."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client for testing."""
        return ShopifyAPIClient(
            shop_domain="test-shop.myshopify.com",
            access_token="test-token"
        )
    
    def test_create_product_integration(self, api_client):
        """Test product creation through API."""
        
        product_data = {
            "title": "Test Product",
            "body_html": "Test description",
            "vendor": "Apple",
            "product_type": "Smartphone"
        }
        
        with requests_mock.Mocker() as m:
            # Mock API response
            m.post(
                "https://test-shop.myshopify.com/admin/api/2025-07/products.json",
                json={
                    "product": {
                        "id": 123456,
                        "title": "Test Product",
                        "handle": "test-product"
                    }
                },
                status_code=201
            )
            
            # Act
            result = api_client.create_product(product_data)
            
            # Assert
            assert result["id"] == 123456
            assert result["title"] == "Test Product"
            
            # Verify request was made correctly
            assert m.call_count == 1
            request = m.request_history[0]
            assert request.json()["product"]["title"] == "Test Product"
    
    def test_rate_limiting_handling(self, api_client):
        """Test rate limiting handling in integration."""
        
        with requests_mock.Mocker() as m:
            # First call returns rate limit error
            m.post(
                "https://test-shop.myshopify.com/admin/api/2025-07/products.json",
                status_code=429,
                headers={"Retry-After": "2"}
            )
            
            # Act & Assert
            with pytest.raises(RateLimitError) as exc_info:
                api_client.create_product({"title": "Test"})
            
            assert exc_info.value.retry_after == 2
```

### Database Integration Testing
```python
class TestRepositoryIntegration:
    """Test repository integration with data persistence."""
    
    @pytest.fixture
    def repository(self):
        """Create repository for testing."""
        # Use test database or in-memory storage
        return ShopifyProductRepository(test_mode=True)
    
    def test_save_and_retrieve_product(self, repository):
        """Test saving and retrieving product data."""
        
        # Arrange
        product = SmartphoneEntity(
            title="Test iPhone",
            brand="Apple",
            model="iPhone 15",
            price=Price(100000, "JPY")
        )
        
        # Act
        saved_product = repository.save(product)
        retrieved_product = repository.get_by_id(saved_product.id)
        
        # Assert
        assert retrieved_product is not None
        assert retrieved_product.title == "Test iPhone"
        assert retrieved_product.brand == "Apple"
        assert retrieved_product.price.amount == 100000
    
    def test_update_product(self, repository):
        """Test updating existing product."""
        
        # Arrange - create initial product
        product = SmartphoneEntity(
            title="Original Title",
            brand="Apple",
            price=Price(100000, "JPY")
        )
        saved_product = repository.save(product)
        
        # Act - update product
        saved_product.title = "Updated Title"
        updated_product = repository.save(saved_product)
        
        # Assert
        retrieved = repository.get_by_id(updated_product.id)
        assert retrieved.title == "Updated Title"
```

## End-to-End Testing Patterns

### User Workflow Testing
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserWorkflows:
    """Test complete user workflows end-to-end."""
    
    @pytest.fixture(scope="session")
    def driver(self):
        """Create web driver for E2E testing."""
        driver = webdriver.Chrome()  # Or use headless option
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    def test_smartphone_product_creation_workflow(self, driver):
        """Test complete smartphone product creation workflow."""
        
        # Navigate to application
        driver.get("http://localhost:8501")
        
        # Select smartphone entry page
        smartphone_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TEXT, "Smartphone Entry"))
        )
        smartphone_button.click()
        
        # Fill in product form
        title_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='product-title']")
        title_input.send_keys("Test iPhone 15 Pro")
        
        price_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='product-price']")
        price_input.send_keys("159800")
        
        # Select template
        template_select = driver.find_element(By.CSS_SELECTOR, "[data-testid='template-select']")
        template_select.send_keys("iPhone 15 Pro Max 256GB [Natural Titanium]")
        
        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='submit-product']")
        submit_button.click()
        
        # Verify success message
        success_message = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".success-message"))
        )
        assert "Product created successfully" in success_message.text
        
        # Verify product appears in session
        session_products = driver.find_elements(By.CSS_SELECTOR, ".session-product")
        assert len(session_products) >= 1
        assert "Test iPhone 15 Pro" in session_products[0].text
```

### API Workflow Testing
```python
class TestAPIWorkflows:
    """Test complete API workflows."""
    
    @pytest.fixture
    def test_data(self):
        """Provide test data for workflows."""
        return {
            "smartphone_data": {
                "title": "Test iPhone 15 Pro",
                "brand": "Apple",
                "model": "iPhone 15 Pro",
                "storage": "256GB",
                "color": "Natural Titanium",
                "price": 159800
            },
            "metafield_data": [
                {
                    "namespace": "custom",
                    "key": "ram_size",
                    "value": '["gid://shopify/Metaobject/123"]',
                    "type": "list.metaobject_reference"
                }
            ]
        }
    
    def test_complete_product_creation_workflow(self, test_data):
        """Test complete product creation with metafields."""
        
        # Initialize services
        api_client = ShopifyAPIClient()
        product_service = ProductService(api_client)
        
        # Create product
        result = product_service.create_smartphone_product(
            test_data["smartphone_data"]
        )
        
        # Verify product creation
        assert "id" in result
        assert result["title"] == test_data["smartphone_data"]["title"]
        
        product_id = result["id"]
        
        # Create metafields
        metafield_result = api_client.create_metafields_for_product(
            product_id, 
            test_data["metafield_data"]
        )
        
        # Verify metafields
        assert metafield_result is not None
        
        # Verify complete product in Shopify
        retrieved_product = api_client.get_product(product_id)
        assert retrieved_product["title"] == test_data["smartphone_data"]["title"]
        
        # Cleanup
        api_client.delete_product(product_id)
```

## Test Data Management Patterns

### Fixture Patterns
```python
@pytest.fixture
def sample_smartphone_data():
    """Provide sample smartphone data for testing."""
    return {
        "title": "iPhone 15 Pro Max 256GB Natural Titanium",
        "brand": "Apple",
        "model": "iPhone 15 Pro Max",
        "storage": "256GB",
        "color": "Natural Titanium",
        "price": 159800,
        "ram": "8GB",
        "display": "6.7-inch Super Retina XDR"
    }

@pytest.fixture
def sample_laptop_data():
    """Provide sample laptop data for testing."""
    return {
        "title": "MacBook Pro 14-inch M3 Pro 512GB Space Black",
        "brand": "Apple",
        "model": "MacBook Pro 14-inch",
        "processor": "Apple M3 Pro",
        "ram": "18GB",
        "storage": "512GB SSD",
        "display": "14-inch Liquid Retina XDR",
        "price": 298800
    }

@pytest.fixture(params=["smartphone", "laptop"])
def product_data(request, sample_smartphone_data, sample_laptop_data):
    """Parameterized fixture for different product types."""
    if request.param == "smartphone":
        return sample_smartphone_data
    else:
        return sample_laptop_data
```

### Test Data Factory Pattern
```python
from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class ProductDataFactory:
    """Factory for creating test product data."""
    
    @staticmethod
    def create_smartphone(
        title: Optional[str] = None,
        brand: str = "Apple",
        model: str = "iPhone 15",
        price: int = 100000,
        **kwargs
    ) -> dict:
        """Create smartphone test data."""
        
        if title is None:
            title = f"{brand} {model} {uuid.uuid4().hex[:8]}"
        
        return {
            "title": title,
            "brand": brand,
            "model": model,
            "price": price,
            "product_type": "Smartphone",
            **kwargs
        }
    
    @staticmethod
    def create_laptop(
        title: Optional[str] = None,
        brand: str = "Apple",
        model: str = "MacBook Pro",
        price: int = 200000,
        **kwargs
    ) -> dict:
        """Create laptop test data."""
        
        if title is None:
            title = f"{brand} {model} {uuid.uuid4().hex[:8]}"
        
        return {
            "title": title,
            "brand": brand,
            "model": model,
            "price": price,
            "product_type": "Laptop",
            "processor": "Apple M3",
            "ram": "16GB",
            "storage": "512GB SSD",
            **kwargs
        }

# Usage
def test_product_creation():
    smartphone_data = ProductDataFactory.create_smartphone(
        brand="Samsung",
        model="Galaxy S24"
    )
    
    laptop_data = ProductDataFactory.create_laptop(
        processor="Intel i7",
        ram="32GB"
    )
```

## Performance Testing Patterns

### Response Time Testing
```python
import time
import pytest

class TestPerformance:
    """Test performance characteristics."""
    
    def test_product_creation_response_time(self):
        """Test that product creation completes within acceptable time."""
        
        product_data = ProductDataFactory.create_smartphone()
        service = ProductService()
        
        start_time = time.time()
        result = service.create_smartphone_product(product_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Assert response time is under 5 seconds
        assert response_time < 5.0, f"Response time {response_time}s exceeds 5s limit"
        assert result is not None
    
    @pytest.mark.parametrize("product_count", [1, 5, 10])
    def test_bulk_product_creation_scaling(self, product_count):
        """Test performance with different product counts."""
        
        products = [
            ProductDataFactory.create_smartphone() 
            for _ in range(product_count)
        ]
        
        service = ProductService()
        
        start_time = time.time()
        results = service.create_multiple_products(products)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time_per_product = total_time / product_count
        
        # Assert reasonable scaling
        assert avg_time_per_product < 10.0, f"Average time per product {avg_time_per_product}s too high"
        assert len(results) == product_count
```

### Memory Usage Testing
```python
import tracemalloc
import gc

def test_memory_usage_during_bulk_operations():
    """Test memory usage during bulk operations."""
    
    # Start memory tracing
    tracemalloc.start()
    
    # Create large dataset
    products = [
        ProductDataFactory.create_smartphone() 
        for _ in range(100)
    ]
    
    service = ProductService()
    
    # Take snapshot before operation
    snapshot1 = tracemalloc.take_snapshot()
    
    # Perform bulk operation
    results = service.create_multiple_products(products)
    
    # Take snapshot after operation
    snapshot2 = tracemalloc.take_snapshot()
    
    # Calculate memory usage
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    total_memory_increase = sum(stat.size_diff for stat in top_stats)
    
    # Assert memory usage is reasonable (< 100MB increase)
    assert total_memory_increase < 100 * 1024 * 1024, f"Memory usage increased by {total_memory_increase} bytes"
    
    # Cleanup
    tracemalloc.stop()
    gc.collect()
```

## Test Organization Patterns

### Test Configuration
```python
# conftest.py
import pytest
import os
from unittest.mock import Mock

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment configuration."""
    
    # Set test environment variables
    os.environ["TESTING"] = "true"
    os.environ["SHOPIFY_SHOP_DOMAIN"] = "test-shop.myshopify.com"
    os.environ["SHOPIFY_ACCESS_TOKEN"] = "test-token"
    
    yield
    
    # Cleanup after all tests
    if "TESTING" in os.environ:
        del os.environ["TESTING"]

@pytest.fixture
def mock_shopify_api():
    """Provide mocked Shopify API client."""
    return Mock(spec=ShopifyAPIClient)

# Pytest configuration
pytest_plugins = [
    "pytest_mock",
    "pytest_asyncio",
    "pytest_cov"
]

# Test markers
pytestmark = pytest.mark.asyncio
```

### Test Categories
```python
# Mark tests by category
@pytest.mark.unit
def test_unit_functionality():
    """Unit test."""
    pass

@pytest.mark.integration
def test_integration_functionality():
    """Integration test."""
    pass

@pytest.mark.e2e
def test_end_to_end_functionality():
    """End-to-end test."""
    pass

@pytest.mark.performance
def test_performance_characteristics():
    """Performance test."""
    pass

@pytest.mark.slow
def test_slow_operation():
    """Test that takes significant time."""
    pass
```

## Coverage and Quality Patterns

### Coverage Configuration
```python
# .coveragerc
[run]
source = .
omit = 
    */tests/*
    */venv/*
    */env/*
    setup.py
    conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

precision = 2
show_missing = True

[html]
directory = htmlcov
```

### Quality Assertions
```python
def test_code_quality_metrics():
    """Test that code quality metrics are maintained."""
    
    # Test coverage is above threshold
    coverage_percent = get_test_coverage()
    assert coverage_percent >= 80, f"Test coverage {coverage_percent}% below 80% threshold"
    
    # Test complexity is reasonable
    complexity_score = get_cyclomatic_complexity()
    assert complexity_score < 10, f"Cyclomatic complexity {complexity_score} too high"
    
    # Test for code smells
    duplication_percent = get_code_duplication()
    assert duplication_percent < 5, f"Code duplication {duplication_percent}% too high"
```

## Common Testing Anti-patterns to Avoid

### ❌ Brittle Tests
```python
# Don't test implementation details
def test_internal_method_calls():
    service = ProductService()
    service._internal_method = Mock()  # Testing private method
    service.create_product({})
    service._internal_method.assert_called_once()  # Brittle
```

### ❌ Slow Tests
```python
# Don't use real API calls in unit tests
def test_product_creation():
    service = ProductService()
    result = service.create_product({})  # Real API call - too slow
```

### ❌ Test Dependencies
```python
# Don't make tests depend on each other
def test_create_product():
    global created_product_id
    created_product_id = create_product()

def test_update_product():
    update_product(created_product_id)  # Depends on previous test
```

### ❌ Poor Test Data
```python
# Don't use unclear or magic test data
def test_validation():
    result = validate_product({"a": "b", "c": 123})  # Unclear data
```

---

**Pattern Version**: 1.0.0
**Last Updated**: 2025-08-02
**Next Review**: 2025-09-02
**Maintainer**: Code Quality Architect