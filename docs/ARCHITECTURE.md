# Architecture Documentation

## Overview

The Shopify Bulk Importer follows a **Clean Architecture** pattern, providing clear separation of concerns and improved maintainability. This document describes the system architecture after Phase 4 improvements.

## Architectural Principles

### 1. Clean Architecture
- **Domain Layer**: Contains business logic independent of external concerns
- **Application Layer**: Orchestrates use cases and workflows
- **Infrastructure Layer**: Handles external dependencies (APIs, databases)
- **Presentation Layer**: User interface (Streamlit)

### 2. Dependency Inversion
- High-level modules don't depend on low-level modules
- Both depend on abstractions (interfaces)
- Dependencies injected through constructor injection

### 3. Single Responsibility
- Each class/module has one reason to change
- Clear separation between business logic and infrastructure concerns

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Streamlit Pages │  │   UI Components │  │  Static Assets  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Application Layer                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Use Case Services│  │   Workflows     │  │  Orchestration  │ │
│  │ (Enhanced       │  │                 │  │                 │ │
│  │  ProductService)│  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Domain Layer                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │    Entities     │  │ Domain Services │  │ Value Objects   │ │
│  │ • SmartphoneEntity │ • ProductDomainService │ • Price      │ │
│  │ • LaptopEntity  │  │ • MetafieldDomainService │ • Metafield │ │
│  │ • Product (Base)│  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Repositories   │  │  External APIs  │  │   Utilities     │ │
│  │ • ProductRepo   │  │ • ShopifyAPI    │  │ • DI Container  │ │
│  │ • MetaobjectRepo│  │ • GraphQL       │  │ • Error Handler │ │
│  │                 │  │                 │  │ • Mappers       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Layer Descriptions

### Domain Layer (`domain/`)

The core business logic layer, independent of external frameworks or infrastructure.

#### Entities (`domain/entities/`)
- **Product**: Abstract base class for all product types
- **SmartphoneEntity**: Smartphone-specific business logic and validation
- **LaptopEntity**: Laptop-specific business logic and validation

#### Domain Services (`domain/services/`)
- **ProductDomainService**: Complex business logic spanning multiple entities
- **MetafieldDomainService**: Metafield mapping and validation logic

#### Value Objects (`domain/value_objects/`)
- **Price**: Immutable price representation with currency handling
- **Metafield**: Immutable metafield data with validation

### Infrastructure Layer (`infrastructure/`)

Handles external dependencies and provides technical implementations.

#### Repositories (`repositories/`)
- **Interfaces**: Abstract repository contracts
- **Implementations**: Shopify-specific repository implementations

#### Dependency Injection (`infrastructure/container.py`)
- **SimpleContainer**: Lightweight DI container
- Service registration and resolution
- Constructor injection support

#### Error Handling (`infrastructure/exceptions.py`, `infrastructure/error_handler.py`)
- **Custom Exception Hierarchy**: Domain, infrastructure, and application exceptions
- **Centralized Error Handler**: Consistent error processing and logging

#### Mappers (`infrastructure/mappers/`)
- **ProductMapper**: Converts between domain entities and API formats

### Application Layer (`services/enhanced_product_service.py`)

Orchestrates business workflows and use cases.

- **EnhancedProductService**: Main application service using clean architecture
- Maintains backward compatibility with existing interfaces
- Coordinates between domain services and repositories

### Presentation Layer (`pages/`, `streamlit_app.py`)

User interface and presentation logic.

- **Streamlit Pages**: UI components for product entry
- **Session Management**: User session and state management

## Key Patterns and Components

### Repository Pattern

Abstracts data access operations behind interfaces:

```python
# Interface
class ProductRepository(ABC):
    @abstractmethod
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

# Implementation
class ShopifyProductRepository(ProductRepository):
    def __init__(self, api_client: ShopifyAPIClient):
        self._api_client = api_client
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._api_client.create_product(product_data)
```

### Dependency Injection

Services receive dependencies through constructor injection:

```python
class EnhancedProductService:
    def __init__(self):
        self.container = get_container()
        self._product_repo = self.container.resolve(ProductRepository)
        self._domain_service = self.container.resolve(ProductDomainService)
```

### Value Objects

Immutable objects representing domain concepts:

```python
@dataclass(frozen=True)
class Price:
    amount: float
    currency: str = "JPY"
    
    def formatted(self) -> str:
        return f"¥{int(self.amount):,}" if self.currency == "JPY" else f"{self.amount:.2f} {self.currency}"
```

### Domain Entities

Rich domain objects with business logic:

```python
@dataclass
class SmartphoneEntity(Product):
    brand: str
    model: Optional[str]
    product_rank: Optional[str]
    
    def validate_business_rules(self) -> List[str]:
        errors = self.validate_common_rules()
        if self.price < 1000:
            errors.append("Smartphone price must be at least ¥1000")
        return errors
```

## Benefits of This Architecture

### 1. Testability
- Domain logic can be unit tested in isolation
- Repository pattern allows easy mocking of external dependencies
- Clear separation of concerns enables focused testing

### 2. Maintainability
- Single responsibility principle enforced at each layer
- Dependencies managed through DI container
- Consistent error handling across the system

### 3. Extensibility
- Easy to add new product types through domain entities
- Repository pattern supports multiple data sources
- New features can be added without touching existing code

### 4. Backward Compatibility
- **EnhancedProductService** maintains the same interface as original services
- Existing Streamlit pages continue to work without modification
- Gradual migration path for adopting new architecture

## Migration Strategy

### Phase 1: Foundation (✅ Complete)
- Implement base repository interfaces and implementations
- Create domain entities and value objects
- Set up dependency injection container
- Implement error handling system

### Phase 2: Service Enhancement (🔄 In Progress)
- Create enhanced services using new architecture
- Maintain backward compatibility with existing interfaces
- Add comprehensive testing

### Phase 3: UI Integration (📋 Planned)
- Update Streamlit pages to use enhanced services
- Improve error handling in UI layer
- Add better user feedback

### Phase 4: Optimization (📋 Planned)
- Performance optimization
- Caching strategies
- Monitoring and metrics

## Configuration

### Container Configuration (`infrastructure/container.py`)

```python
def configure_container() -> SimpleContainer:
    container = SimpleContainer()
    
    # Infrastructure
    container.register_factory(ShopifyAPIClient, lambda: ShopifyAPIClient())
    
    # Repositories
    container.register(ProductRepository, ShopifyProductRepository)
    container.register(MetaobjectRepository, ShopifyMetaobjectRepository)
    
    # Domain Services
    container.register_instance(ProductDomainService, ProductDomainService())
    container.register_instance(MetafieldDomainService, MetafieldDomainService())
    
    return container
```

## Error Handling

### Exception Hierarchy

```
Exception
├── DomainException
│   ├── ValidationException
│   └── BusinessRuleException
├── InfrastructureException
│   ├── ExternalServiceException
│   └── RepositoryException
└── ApplicationException
```

### Error Processing

```python
def handle_error(exception: Exception, context: ErrorContext) -> Dict[str, Any]:
    # Create standardized error response
    # Log with appropriate level
    # Track error statistics
    # Return formatted response
```

## Performance Considerations

### Lazy Loading
- Services are created only when needed
- Singleton pattern for expensive resources

### Caching
- Metaobject GID mappings cached in repository
- Container caches singleton instances

### Async Support
- Repository interfaces designed for async operations
- Future-ready for async Shopify API integration

## Security Considerations

### Input Validation
- Domain entities validate business rules
- Value objects ensure data integrity
- Repository layer sanitizes inputs

### Error Information
- Sensitive information not exposed in error responses
- Stack traces only included in development mode
- Proper logging of security-relevant events

## Monitoring and Observability

### Error Tracking
- Centralized error handler tracks all exceptions  
- Error statistics collection
- Trace IDs for error correlation

### Logging
- Structured logging with context information
- Different log levels for different error types
- Integration with external logging systems

## Future Enhancements

### 1. CQRS Pattern
- Separate command and query responsibilities
- Improved scalability for read-heavy operations

### 2. Event Sourcing
- Track all changes as events
- Better audit trail and debugging

### 3. Microservices
- Split into focused services
- Independent scaling and deployment

### 4. GraphQL Integration
- Direct GraphQL client for better performance
- Reduced API calls and improved efficiency

---

**Last Updated**: 2025-07-31  
**Version**: 2.0.0 (Phase 4 Architecture Improvements)  
**Next Review**: Phase 5 Implementation