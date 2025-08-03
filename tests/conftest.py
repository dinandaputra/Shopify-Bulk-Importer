"""
Pytest configuration and shared fixtures for the Shopify Bulk Importer test suite.

This module provides global test configuration, shared fixtures, and utilities
for all test modules in the project.
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch
from typing import Generator, Dict, Any

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test environment variables
os.environ.update({
    'SHOPIFY_ACCESS_TOKEN': 'test_access_token',
    'SHOPIFY_API_KEY': 'test_api_key', 
    'SHOPIFY_API_SECRET': 'test_api_secret',
    'SHOPIFY_SHOP_DOMAIN': 'test-shop.myshopify.com'
})


@pytest.fixture(scope="session")
def test_config() -> Dict[str, str]:
    """Test configuration for the entire test session."""
    return {
        'shop_domain': 'test-shop.myshopify.com',
        'access_token': 'test_access_token',
        'api_key': 'test_api_key',
        'api_secret': 'test_api_secret'
    }


@pytest.fixture
def mock_shopify_api():
    """Mock Shopify API client for testing."""
    with patch('services.shopify_api.requests') as mock_requests:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'product': {
                'id': 123456789,
                'title': 'Test Product',
                'variants': [{'id': 987654321}]
            }
        }
        mock_requests.post.return_value = mock_response
        mock_requests.get.return_value = mock_response
        mock_requests.put.return_value = mock_response
        yield mock_requests


@pytest.fixture
def sample_smartphone_data() -> Dict[str, Any]:
    """Sample smartphone data for testing."""
    return {
        'title': 'iPhone 14 Pro 128GB Space Black',
        'brand': 'Apple',
        'model': 'iPhone 14 Pro',
        'color': 'Space Black',
        'storage': '128GB',
        'price': 120000,
        'product_rank': 'A',
        'sim_carriers': ['docomo', 'au', 'softbank'],
        'inclusions': ['charger', 'cable', 'manual'],
        'ram_size': '6GB',
        'minus': []
    }


@pytest.fixture
def sample_laptop_data() -> Dict[str, Any]:
    """Sample laptop data for testing."""
    return {
        'title': 'MacBook Pro 14-inch M3 Pro',
        'brand': 'Apple',
        'price': 280000,
        'product_rank': 'A',
        'processor': 'Apple M3 Pro',
        'ram': '18GB',
        'storage': '512GB SSD',
        'display': '14.2-inch Liquid Retina XDR',
        'graphics': 'Apple M3 Pro GPU',
        'os': 'macOS Sonoma',
        'keyboard': 'US',
        'inclusions': ['adapter', 'cable', 'manual']
    }


@pytest.fixture
def mock_dependency_container():
    """Mock dependency injection container."""
    from infrastructure.container import SimpleContainer
    
    container = SimpleContainer()
    
    # Mock repositories
    mock_product_repo = Mock()
    mock_metaobject_repo = Mock()
    
    container.register('product_repository', lambda: mock_product_repo)
    container.register('metaobject_repository', lambda: mock_metaobject_repo)
    
    return container


@pytest.fixture
def mock_shopify_response():
    """Mock successful Shopify API response."""
    return {
        'product': {
            'id': 123456789,
            'title': 'Test Product',
            'handle': 'test-product',
            'status': 'active',
            'variants': [
                {
                    'id': 987654321,
                    'title': 'Default Title',
                    'price': '100.00',
                    'inventory_quantity': 10
                }
            ],
            'images': [],
            'metafields': []
        }
    }


@pytest.fixture
def mock_metaobject_response():
    """Mock metaobject query response."""
    return {
        'data': {
            'metaobjects': {
                'edges': [
                    {
                        'node': {
                            'id': 'gid://shopify/Metaobject/123',
                            'fields': [
                                {
                                    'key': 'name',
                                    'value': 'Test Value'
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically set up test environment for all tests."""
    # Ensure test environment variables are set
    required_vars = [
        'SHOPIFY_ACCESS_TOKEN',
        'SHOPIFY_API_KEY',
        'SHOPIFY_API_SECRET', 
        'SHOPIFY_SHOP_DOMAIN'
    ]
    
    for var in required_vars:
        if not os.environ.get(var):
            os.environ[var] = f'test_{var.lower()}'


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as interacting with Shopify API"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add automatic markers."""
    for item in items:
        # Add markers based on test location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
            
        # Add API marker for tests that use Shopify API
        if "api" in item.name.lower() or "shopify" in item.name.lower():
            item.add_marker(pytest.mark.api)


@pytest.fixture
def mock_streamlit_session_state():
    """Mock Streamlit session state for laptop entry testing."""
    class MockSessionState:
        def __init__(self):
            self._state = {}
        
        def __getattr__(self, key):
            return self._state.get(key)
        
        def __setattr__(self, key, value):
            if key.startswith('_'):
                super().__setattr__(key, value)
            else:
                self._state[key] = value
        
        def __contains__(self, key):
            return key in self._state
        
        def __getitem__(self, key):
            return self._state[key]
        
        def __setitem__(self, key, value):
            self._state[key] = value
        
        def get(self, key, default=None):
            return self._state.get(key, default)
        
        def clear(self):
            self._state.clear()
        
        def keys(self):
            return self._state.keys()
        
        def values(self):
            return self._state.values()
        
        def items(self):
            return self._state.items()
    
    return MockSessionState()


@pytest.fixture
def sample_laptop_templates():
    """Sample laptop templates for testing unified fuzzy search."""
    return [
        "ASUS ROG Strix G15 [i7-12700H, RTX 4060, 16GB, 512GB SSD, 15.6\" 144Hz]",
        "Dell XPS 13 [i5-1340P, Intel Iris Xe, 8GB, 512GB SSD, 13.4\" FHD+]",
        "HP Pavilion Gaming [i5-12500H, GTX 1650, 16GB, 512GB SSD, 15.6\" 144Hz]",
        "MacBook Pro 14 [M3 Pro, 18GB, 512GB SSD, 14.2\" Liquid Retina XDR]",
        "ThinkPad X1 Carbon [i7-1365U, Intel Iris Xe, 16GB, 1TB SSD, 14\" WUXGA]"
    ]


@pytest.fixture
def sample_extracted_laptop_info():
    """Sample extracted laptop information for testing template processing."""
    return {
        "title": "ASUS ROG Strix G15",
        "brand": "ASUS",
        "cpu": "Intel Core i7-12700H",
        "gpu": "NVIDIA GeForce RTX 4060",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "15.6-inch 144Hz",
        "collections": ["All Products", "ASUS Laptops", "Gaming Laptops"]
    }


@pytest.fixture
def laptop_form_field_keys():
    """Standard laptop form field keys for testing form clearing."""
    return [
        "laptop_title_input", "laptop_price_input", "laptop_rank_input",
        "laptop_cpu_input", "laptop_ram_input", "laptop_gpu_input", 
        "laptop_integrated_gpu_input", "laptop_display_input", "laptop_storage_input",
        "laptop_color_input", "laptop_inclusions_input", "laptop_minus_input", 
        "laptop_collections_input"
    ]


@pytest.fixture
def mock_laptop_template_functions():
    """Mock template functions for testing without external dependencies."""
    def mock_get_laptop_template_suggestions():
        return [
            "ASUS ROG Strix G15 [i7-12700H, RTX 4060, 16GB, 512GB SSD, 15.6\" 144Hz]",
            "Dell XPS 13 [i5-1340P, Intel Iris Xe, 8GB, 512GB SSD, 13.4\" FHD+]",
            "HP Pavilion Gaming [i5-12500H, GTX 1650, 16GB, 512GB SSD, 15.6\" 144Hz]"
        ]
    
    def mock_extract_info_from_template(template):
        if "ASUS ROG" in template:
            return {
                "title": "ASUS ROG Strix G15",
                "brand": "ASUS",
                "cpu": "Intel Core i7-12700H",
                "gpu": "NVIDIA GeForce RTX 4060",
                "ram": "16GB",
                "storage": "512GB SSD",
                "display": "15.6-inch 144Hz"
            }
        elif "Dell XPS" in template:
            return {
                "title": "Dell XPS 13",
                "brand": "Dell",
                "cpu": "Intel Core i5-1340P",
                "integrated_graphics": "Intel Iris Xe",
                "ram": "8GB",
                "storage": "512GB SSD",
                "display": "13.4-inch FHD+"
            }
        return {}
    
    return {
        'get_laptop_template_suggestions': mock_get_laptop_template_suggestions,
        'extract_info_from_template': mock_extract_info_from_template
    }


@pytest.fixture
def performance_test_config():
    """Configuration for performance testing."""
    return {
        'max_load_time': 3.0,  # seconds
        'max_search_response_time': 1.0,  # seconds
        'template_count': 162,  # expected number of laptop templates
        'max_memory_usage': 50 * 1024 * 1024,  # 50MB in bytes
        'max_ui_response_time': 0.5  # seconds for UI operations
    }