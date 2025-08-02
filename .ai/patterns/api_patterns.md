# Shopify API Integration Patterns

This document establishes standardized patterns for interacting with the Shopify API, ensuring consistency, reliability, and maintainability across the codebase.

## Overview

**Purpose**: Standardized Shopify API integration patterns
**Scope**: All Shopify REST and GraphQL interactions
**Maintainer**: Shopify API Developer

## Core Principles

### 1. API Client Abstraction
Always use the centralized API client rather than direct HTTP calls.

```python
# ✅ Correct: Use centralized client
from services.shopify_api import ShopifyAPIClient

client = ShopifyAPIClient()
result = client.create_product(product_data)

# ❌ Incorrect: Direct HTTP calls
import requests
response = requests.post(f"https://{shop_domain}/admin/api/2025-07/products.json")
```

### 2. Error Handling Consistency
Use standardized error handling patterns with proper exception types.

```python
# ✅ Correct: Standardized error handling
from infrastructure.exceptions import ShopifyAPIError, RateLimitError

try:
    result = client.create_product(product_data)
    return result
except RateLimitError as e:
    # Handle rate limiting with backoff
    await self._handle_rate_limit(e)
    return await self.create_product(product_data)  # Retry
except ShopifyAPIError as e:
    # Log and re-raise with context
    logger.error(f"Failed to create product: {e}")
    raise ProductCreationError(f"Could not create product: {e}") from e
```

### 3. Rate Limiting Respect
Always implement rate limiting awareness and backoff strategies.

```python
# ✅ Correct: Rate limit handling
async def _handle_rate_limit(self, error: RateLimitError):
    retry_after = error.retry_after or 2
    backoff_time = min(retry_after * (2 ** self.retry_count), 60)
    logger.warning(f"Rate limited. Backing off for {backoff_time}s")
    await asyncio.sleep(backoff_time)
    self.retry_count += 1
```

## API Selection Patterns

### REST vs GraphQL Decision Matrix

| Operation Type | Preferred API | Reason |
|---------------|---------------|---------|
| Simple CRUD | REST | Simpler implementation |
| Complex queries | GraphQL | More efficient data fetching |
| Bulk operations | GraphQL | Better performance |
| Metafield operations | GraphQL | More flexible querying |
| Product creation | REST | Established patterns |
| Metaobject queries | GraphQL | Native support |

### REST API Patterns

#### Product Creation Pattern
```python
def create_product(self, product_data: Dict) -> Dict:
    """Create a product using REST API."""
    
    # Validate input data
    validated_data = self._validate_product_data(product_data)
    
    # Prepare request
    url = f"{self.base_url}/products.json"
    payload = {"product": validated_data}
    
    # Make request with retry logic
    response = self._make_request_with_retry("POST", url, json=payload)
    
    # Process response
    if response.status_code == 201:
        return response.json()["product"]
    else:
        raise ShopifyAPIError(f"Failed to create product: {response.text}")
```

#### Metafield Creation Pattern
```python
def create_metafield(self, owner_id: str, owner_type: str, metafield_data: Dict) -> Dict:
    """Create a metafield using REST API."""
    
    url = f"{self.base_url}/{owner_type.lower()}s/{owner_id}/metafields.json"
    payload = {"metafield": metafield_data}
    
    try:
        response = self._make_request_with_retry("POST", url, json=payload)
        if response.status_code == 201:
            return response.json()["metafield"]
        else:
            # Log but don't fail - metafields are optional
            logger.warning(f"Failed to create metafield: {response.text}")
            return None
    except Exception as e:
        logger.warning(f"Metafield creation failed: {e}")
        return None
```

### GraphQL API Patterns

#### Query Pattern with Error Handling
```python
def query_metaobjects(self, definition_type: str, limit: int = 50) -> List[Dict]:
    """Query metaobjects using GraphQL."""
    
    query = """
    query getMetaobjects($type: String!, $first: Int!) {
        metaobjects(type: $type, first: $first) {
            edges {
                node {
                    id
                    handle
                    displayName
                    fields {
                        key
                        value
                    }
                }
            }
        }
    }
    """
    
    variables = {"type": definition_type, "first": limit}
    
    try:
        result = self._execute_graphql_query(query, variables)
        
        # Check for GraphQL errors
        if "errors" in result:
            raise ShopifyAPIError(f"GraphQL errors: {result['errors']}")
        
        # Extract data
        edges = result.get("data", {}).get("metaobjects", {}).get("edges", [])
        return [edge["node"] for edge in edges]
        
    except Exception as e:
        logger.error(f"Failed to query metaobjects: {e}")
        raise MetaobjectQueryError(f"Could not query metaobjects: {e}") from e
```

#### Mutation Pattern with Validation
```python
def create_product_with_metafields(self, product_data: Dict, metafields: List[Dict]) -> Dict:
    """Create product with metafields using GraphQL."""
    
    mutation = """
    mutation productCreate($input: ProductInput!, $metafields: [MetafieldsSetInput!]!) {
        productCreate(input: $input) {
            product {
                id
                handle
                title
            }
            userErrors {
                field
                message
            }
        }
        metafieldsSet(metafields: $metafields) {
            metafields {
                id
                key
                value
            }
            userErrors {
                field
                message
            }
        }
    }
    """
    
    variables = {
        "input": product_data,
        "metafields": metafields
    }
    
    result = self._execute_graphql_mutation(mutation, variables)
    
    # Check for user errors in both operations
    product_errors = result.get("data", {}).get("productCreate", {}).get("userErrors", [])
    metafield_errors = result.get("data", {}).get("metafieldsSet", {}).get("userErrors", [])
    
    if product_errors:
        raise ProductCreationError(f"Product creation failed: {product_errors}")
    
    if metafield_errors:
        logger.warning(f"Some metafields failed to create: {metafield_errors}")
    
    return result["data"]["productCreate"]["product"]
```

## Authentication Patterns

### Token Management
```python
class ShopifyAuthenticator:
    """Manages Shopify API authentication."""
    
    def __init__(self):
        self.access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
        self.shop_domain = os.getenv("SHOPIFY_SHOP_DOMAIN")
        
        if not self.access_token or not self.shop_domain:
            raise ConfigurationError("Missing Shopify credentials")
    
    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        return {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def validate_token(self) -> bool:
        """Validate the access token by making a test request."""
        try:
            # Test with a simple API call
            url = f"https://{self.shop_domain}/admin/api/2025-07/shop.json"
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            return response.status_code == 200
        except Exception:
            return False
```

## Data Validation Patterns

### Input Validation
```python
from pydantic import BaseModel, validator
from typing import Optional, List

class ProductCreateData(BaseModel):
    """Validates product creation data."""
    
    title: str
    body_html: Optional[str] = ""
    vendor: str
    product_type: str
    tags: Optional[str] = ""
    published: bool = False
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('vendor')
    def vendor_must_be_valid(cls, v):
        allowed_vendors = ['Apple', 'Samsung', 'Google', 'OnePlus']
        if v not in allowed_vendors:
            raise ValueError(f'Vendor must be one of: {allowed_vendors}')
        return v

# Usage
def create_product(self, product_data: Dict) -> Dict:
    # Validate input
    validated_data = ProductCreateData(**product_data)
    
    # Convert to dict for API
    api_data = validated_data.dict(exclude_none=True)
    
    # Make API call
    return self._create_product_via_api(api_data)
```

### Response Validation
```python
def _validate_api_response(self, response: requests.Response) -> Dict:
    """Validate and parse API response."""
    
    # Check HTTP status
    if not response.ok:
        raise ShopifyAPIError(
            f"API request failed: {response.status_code} - {response.text}"
        )
    
    # Parse JSON
    try:
        data = response.json()
    except ValueError as e:
        raise ShopifyAPIError(f"Invalid JSON response: {e}")
    
    # Check for API errors
    if "errors" in data:
        raise ShopifyAPIError(f"API errors: {data['errors']}")
    
    return data
```

## Error Handling Patterns

### Exception Hierarchy
```python
class ShopifyAPIError(Exception):
    """Base exception for Shopify API errors."""
    pass

class RateLimitError(ShopifyAPIError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str, retry_after: int = None):
        super().__init__(message)
        self.retry_after = retry_after

class AuthenticationError(ShopifyAPIError):
    """Raised when authentication fails."""
    pass

class ValidationError(ShopifyAPIError):
    """Raised when data validation fails."""
    pass

class ResourceNotFoundError(ShopifyAPIError):
    """Raised when requested resource is not found."""
    pass
```

### Retry Logic Pattern
```python
import asyncio
from functools import wraps

def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator for retrying operations with exponential backoff."""
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except RateLimitError as e:
                    last_exception = e
                    if attempt == max_retries:
                        break
                    
                    # Calculate backoff time
                    delay = base_delay * (2 ** attempt)
                    if e.retry_after:
                        delay = max(delay, e.retry_after)
                    
                    logger.warning(f"Rate limited, retrying in {delay}s (attempt {attempt + 1})")
                    await asyncio.sleep(delay)
                    
                except (AuthenticationError, ValidationError):
                    # Don't retry these errors
                    raise
                except ShopifyAPIError as e:
                    last_exception = e
                    if attempt == max_retries:
                        break
                    
                    # Retry with backoff for other API errors
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"API error, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
            
            # All retries exhausted
            raise last_exception
        
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3)
async def create_product_with_retry(self, product_data: Dict) -> Dict:
    return await self.api_client.create_product(product_data)
```

## Metafield Management Patterns

### Metafield Creation with References
```python
def create_metafield_with_reference(
    self, 
    owner_id: str, 
    owner_type: str,
    metafield_key: str,
    metaobject_gids: List[str],
    namespace: str = "custom"
) -> Optional[Dict]:
    """Create a metafield with metaobject references."""
    
    # Format value as JSON array for list.metaobject_reference
    if len(metaobject_gids) == 1:
        # Single reference
        value = f'["{metaobject_gids[0]}"]'
    else:
        # Multiple references
        gid_strings = [f'"{gid}"' for gid in metaobject_gids]
        value = f'[{", ".join(gid_strings)}]'
    
    metafield_data = {
        "namespace": namespace,
        "key": metafield_key,
        "value": value,
        "type": "list.metaobject_reference"
    }
    
    return self.create_metafield(owner_id, owner_type, metafield_data)
```

### Protected System Pattern ⚠️
```python
def assign_metafields_to_variants(self, variant_metafield_data: List[Dict]) -> Dict:
    """
    Assign metafields to product variants using GraphQL.
    
    WARNING: This is a protected system - DO NOT MODIFY without approval.
    This implementation is working and critical for SIM carrier functionality.
    """
    
    mutation = """
    mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
        metafieldsSet(metafields: $metafields) {
            metafields {
                id
                key
                namespace
                value
                ownerType
                createdAt
            }
            userErrors {
                field
                message
            }
        }
    }
    """
    
    variables = {"metafields": variant_metafield_data}
    
    try:
        result = self._execute_graphql_mutation(mutation, variables)
        
        # Check for errors
        user_errors = result.get("data", {}).get("metafieldsSet", {}).get("userErrors", [])
        if user_errors:
            logger.error(f"GraphQL metafield assignment errors: {user_errors}")
            raise ShopifyAPIError(f"Metafield assignment failed: {user_errors}")
        
        metafields = result.get("data", {}).get("metafieldsSet", {}).get("metafields", [])
        logger.info(f"Successfully created {len(metafields)} variant metafields")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to assign variant metafields: {e}")
        raise MetafieldAssignmentError(f"Could not assign variant metafields: {e}") from e
```

## Performance Optimization Patterns

### Batch Operations
```python
def batch_create_metafields(self, metafield_requests: List[Dict], batch_size: int = 10) -> List[Dict]:
    """Create metafields in batches to optimize performance."""
    
    results = []
    
    for i in range(0, len(metafield_requests), batch_size):
        batch = metafield_requests[i:i + batch_size]
        
        # Use GraphQL for batch operations
        mutation = """
        mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
            metafieldsSet(metafields: $metafields) {
                metafields {
                    id
                    key
                    value
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        variables = {"metafields": batch}
        result = self._execute_graphql_mutation(mutation, variables)
        
        # Process batch results
        batch_metafields = result.get("data", {}).get("metafieldsSet", {}).get("metafields", [])
        results.extend(batch_metafields)
        
        # Rate limiting consideration
        if i + batch_size < len(metafield_requests):
            time.sleep(0.5)  # Brief pause between batches
    
    return results
```

### Caching Pattern
```python
from functools import lru_cache
import time

class ShopifyAPIClient:
    def __init__(self):
        self._metaobject_cache = {}
        self._cache_ttl = 300  # 5 minutes
    
    def get_metaobjects_cached(self, definition_type: str) -> List[Dict]:
        """Get metaobjects with caching."""
        
        cache_key = f"metaobjects_{definition_type}"
        now = time.time()
        
        # Check cache
        if cache_key in self._metaobject_cache:
            cached_data, timestamp = self._metaobject_cache[cache_key]
            if now - timestamp < self._cache_ttl:
                return cached_data
        
        # Fetch fresh data
        metaobjects = self.query_metaobjects(definition_type)
        
        # Update cache
        self._metaobject_cache[cache_key] = (metaobjects, now)
        
        return metaobjects
    
    def invalidate_cache(self, cache_key: str = None):
        """Invalidate cache entries."""
        if cache_key:
            self._metaobject_cache.pop(cache_key, None)
        else:
            self._metaobject_cache.clear()
```

## Logging and Monitoring Patterns

### API Call Logging
```python
import logging
from functools import wraps

def log_api_call(func):
    """Decorator to log API calls with timing and results."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        method_name = func.__name__
        
        try:
            # Log request
            logger.info(f"Starting API call: {method_name}")
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Log success
            duration = time.time() - start_time
            logger.info(f"API call succeeded: {method_name} ({duration:.2f}s)")
            
            return result
            
        except Exception as e:
            # Log failure
            duration = time.time() - start_time
            logger.error(f"API call failed: {method_name} ({duration:.2f}s) - {e}")
            raise
    
    return wrapper

# Usage
@log_api_call
def create_product(self, product_data: Dict) -> Dict:
    # Implementation here
    pass
```

### Performance Monitoring
```python
class APIMetrics:
    """Track API performance metrics."""
    
    def __init__(self):
        self.call_counts = {}
        self.response_times = {}
        self.error_counts = {}
    
    def record_call(self, endpoint: str, duration: float, success: bool):
        """Record an API call metric."""
        
        # Update call count
        self.call_counts[endpoint] = self.call_counts.get(endpoint, 0) + 1
        
        # Update response times
        if endpoint not in self.response_times:
            self.response_times[endpoint] = []
        self.response_times[endpoint].append(duration)
        
        # Update error count
        if not success:
            self.error_counts[endpoint] = self.error_counts.get(endpoint, 0) + 1
    
    def get_stats(self) -> Dict:
        """Get performance statistics."""
        stats = {}
        
        for endpoint in self.call_counts:
            call_count = self.call_counts[endpoint]
            response_times = self.response_times.get(endpoint, [])
            error_count = self.error_counts.get(endpoint, 0)
            
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            error_rate = (error_count / call_count) * 100 if call_count > 0 else 0
            
            stats[endpoint] = {
                "call_count": call_count,
                "avg_response_time": avg_response_time,
                "error_rate": error_rate
            }
        
        return stats
```

## Common Anti-patterns to Avoid

### ❌ Direct HTTP Calls
```python
# Don't do this
import requests
response = requests.post(f"https://{shop}/admin/api/2025-07/products.json")
```

### ❌ Ignoring Rate Limits
```python
# Don't do this
for product in products:
    create_product(product)  # Will hit rate limits
```

### ❌ Poor Error Handling
```python
# Don't do this
try:
    result = api_call()
except:
    pass  # Silent failures are bad
```

### ❌ Hardcoded Values
```python
# Don't do this
url = "https://shop.myshopify.com/admin/api/2025-07/products.json"
```

### ❌ Inconsistent Data Formats
```python
# Don't do this - mixing string and array formats
value1 = "gid://shopify/Metaobject/123"  # String
value2 = ["gid://shopify/Metaobject/456"]  # Array
```

---

**Pattern Version**: 1.0.0
**Last Updated**: 2025-08-02
**Next Review**: 2025-09-02
**Maintainer**: Shopify API Developer