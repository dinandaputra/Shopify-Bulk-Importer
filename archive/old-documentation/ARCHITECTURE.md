# Architecture Documentation

## System Overview

The Shopify Bulk Importer is a Streamlit-based web application designed with a modular architecture that separates concerns between UI, business logic, and external integrations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │ streamlit_app.py│  │smartphone_entry │  │laptop_entry│  │
│  └────────┬────────┘  └────────┬────────┘  └─────┬──────┘  │
└───────────┼────────────────────┼──────────────────┼─────────┘
            │                    │                   │
┌───────────▼────────────────────▼───────────────────▼─────────┐
│                        Service Layer                          │
│  ┌──────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │product_service│  │metaobject_service│  │image_service   │  │
│  └──────┬───────┘  └────────┬────────┘  └───────┬────────┘  │
│  ┌──────▼───────┐  ┌────────▼────────┐  ┌───────▼────────┐  │
│  │shopify_api   │  │validation_service│  │export_service  │  │
│  └──────────────┘  └─────────────────┘  └────────────────┘  │
└───────────┬──────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────┐
│                        Data Layer                             │
│  ┌──────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │Models        │  │Configuration     │  │Database        │  │
│  │- smartphone  │  │- master_data     │  │- handle_counter│  │
│  │- laptop      │  │- shopify_config  │  │- session_state │  │
│  └──────────────┘  └─────────────────┘  └────────────────┘  │
└──────────────────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────┐
│                    External Systems                           │
│  ┌──────────────────────┐  ┌─────────────────────────────┐  │
│  │ Shopify REST API     │  │ Shopify GraphQL API       │  │
│  │ - Product creation   │  │ - Metafield assignment    │  │
│  │ - Inventory updates  │  │ - Metaobject queries      │  │
│  └──────────────────────┘  └─────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Presentation Layer (UI)

**Technology**: Streamlit

**Components**:
- `streamlit_app.py`: Main entry point with navigation
- `pages/smartphone_entry.py`: Smartphone product entry interface
- `pages/laptop_entry.py`: Laptop product entry interface

**Responsibilities**:
- User input collection
- Data display and formatting
- Session state management
- Error message presentation

### 2. Service Layer (Business Logic)

**Key Services**:

#### product_service.py
- Orchestrates product creation workflow
- Coordinates between multiple services
- Handles business rule enforcement

#### shopify_api.py
- Direct Shopify API communication
- REST and GraphQL endpoint management
- Authentication and rate limiting
- Error handling and retries

#### metaobject_service.py
- Metaobject reference resolution
- Metafield data formatting
- GraphQL query construction

#### validation_service.py
- Input validation beyond model constraints
- Business rule enforcement
- Data consistency checks

#### image_service.py
- Image upload to Shopify CDN
- Image URL generation
- Multi-image handling

#### export_service.py
- CSV generation for manual import
- Data formatting for Shopify import
- Fallback workflow support

### 3. Data Layer

**Models** (Pydantic):
- `smartphone.py`: Smartphone product schema with validation
- `laptop.py`: Laptop product schema with specifications

**Configuration**:
- `master_data.py`: Product templates and predefined data
- `shopify_config.py`: API configuration and environment settings
- `laptop_specs.py`: Laptop model specifications database
- Metafield mapping files for object reference lookups

**Persistence**:
- `handle_counter.json`: Daily counter persistence
- Streamlit session state: Temporary product storage

### 4. Integration Layer

**Shopify REST API**:
- Product creation and updates
- Inventory management
- Basic resource operations

**Shopify GraphQL API**:
- Metafield assignment (metafieldsSet mutation)
- Metaobject queries and creation
- Complex data relationships

## Data Flow

### Product Creation Flow

```
1. User Input (UI Layer)
   ↓
2. Validation (Pydantic Model)
   ↓
3. Business Logic (Product Service)
   ↓
4. API Preparation (Service Layer)
   ↓
5. Shopify API Call (REST/GraphQL)
   ↓
6. Response Processing
   ↓
7. UI Update (Success/Error)
```

### Metafield Assignment Flow

```
1. Product Created (REST API)
   ↓
2. Extract Product/Variant IDs
   ↓
3. Map Values to Metaobject GIDs
   ↓
4. Construct GraphQL Mutation
   ↓
5. Execute metafieldsSet
   ↓
6. Verify Assignment
```

## Key Design Patterns

### 1. Service-Oriented Architecture
- Each service has a single responsibility
- Services communicate through well-defined interfaces
- Loose coupling between components

### 2. Repository Pattern (Planned)
- Abstraction over data access
- Enables testing with mock implementations
- Supports future data source changes

### 3. Factory Pattern
- Template system for product creation
- Dynamic model generation based on selections

### 4. Observer Pattern
- Session state updates trigger UI refreshes
- Event-driven error handling

## Configuration Management

### Environment Variables
- API credentials stored securely
- Environment-specific settings
- No hardcoded secrets

### Feature Flags (Planned)
```python
FEATURES = {
    'new_ui': False,
    'bulk_operations': False,
    'advanced_search': False
}
```

## Security Considerations

### API Security
- Access tokens never exposed in UI
- HTTPS-only communication
- Rate limiting compliance

### Data Validation
- Input sanitization at every layer
- Pydantic models enforce type safety
- Business rule validation

### Session Management
- Isolated user sessions
- Automatic cleanup
- No persistent user data

## Performance Optimizations

### Current Optimizations
- Lazy loading of configuration data
- Efficient GraphQL queries
- Session-based caching

### Planned Optimizations
- Redis caching for metaobject lookups
- Batch API operations
- Async processing for large operations

## Error Handling Strategy

### Layers of Error Handling

1. **Model Validation**: Pydantic ValidationError
2. **Service Layer**: Custom exceptions with context
3. **API Layer**: Shopify-specific error handling
4. **UI Layer**: User-friendly error messages

### Error Recovery
- Automatic retry for transient failures
- Graceful degradation (CSV export fallback)
- Detailed logging for debugging

## Testing Strategy

### Unit Tests
- Model validation tests
- Service logic tests
- Utility function tests

### Integration Tests
- API interaction tests
- End-to-end workflow tests
- Error scenario tests

### Performance Tests
- Load testing for concurrent users
- API rate limit compliance
- Response time benchmarks

## Deployment Architecture

### Current Setup
- Local development environment
- Direct API connection to Shopify
- File-based configuration

### Production Recommendations
- Containerized deployment (Docker)
- Environment-based configuration
- Centralized logging
- Monitoring and alerting
- Load balancing for multiple instances

## Future Architecture Improvements

### Phase 1: Code Organization
- Implement repository pattern
- Add dependency injection
- Create domain layer

### Phase 2: Scalability
- Add caching layer
- Implement message queuing
- Support horizontal scaling

### Phase 3: Advanced Features
- Webhook integration
- Real-time inventory sync
- Multi-store support
- Advanced analytics

## Technology Decisions

### Why Streamlit?
- Rapid development
- Built-in session management
- Native Python integration
- Good for internal tools

### Why Pydantic?
- Type safety
- Automatic validation
- JSON schema generation
- Excellent error messages

### Why REST + GraphQL?
- REST for simple operations
- GraphQL for complex metafield operations
- Best of both worlds approach

## Maintenance Considerations

### Code Quality
- Type hints throughout
- Comprehensive documentation
- Consistent naming conventions
- Regular refactoring

### Monitoring
- API call logging
- Error tracking
- Performance metrics
- User activity tracking

### Updates
- Shopify API version management
- Dependency updates
- Security patches
- Feature additions

This architecture provides a solid foundation for the current application while allowing for future growth and improvements.