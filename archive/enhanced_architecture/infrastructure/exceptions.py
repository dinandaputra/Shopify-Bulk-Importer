"""
Custom exception hierarchy for Shopify Bulk Importer.

This module defines custom exceptions for different layers of the application,
providing consistent error handling and detailed error information.
"""

from typing import Optional, Dict, Any


class DomainException(Exception):
    """
    Base exception for domain layer errors.
    
    This exception and its subclasses represent business logic errors
    and domain rule violations.
    """
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 context: Optional[Dict[str, Any]] = None):
        """
        Initialize domain exception.
        
        Args:
            message: Error message
            error_code: Optional error code for categorization
            context: Optional context information
        """
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}


class ValidationException(DomainException):
    """Exception for validation errors."""
    
    def __init__(self, field: str, message: str, value: Any = None):
        """
        Initialize validation exception.
        
        Args:
            field: Field that failed validation
            message: Validation error message
            value: The invalid value
        """
        super().__init__(f"Validation error on field '{field}': {message}")
        self.field = field
        self.value = value
        self.error_code = "VALIDATION_ERROR"


class BusinessRuleException(DomainException):
    """Exception for business rule violations."""
    
    def __init__(self, rule: str, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize business rule exception.
        
        Args:
            rule: The business rule that was violated
            message: Error message
            context: Optional context information
        """
        super().__init__(f"Business rule violation '{rule}': {message}")
        self.rule = rule
        self.error_code = "BUSINESS_RULE_VIOLATION"
        self.context = context or {}


class InfrastructureException(Exception):
    """
    Base exception for infrastructure layer errors.
    
    This exception and its subclasses represent infrastructure-related
    errors such as database, API, or external service failures.
    """
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 original_exception: Optional[Exception] = None):
        """
        Initialize infrastructure exception.
        
        Args:
            message: Error message
            error_code: Optional error code
            original_exception: The original exception that caused this error
        """
        super().__init__(message)
        self.error_code = error_code
        self.original_exception = original_exception


class ExternalServiceException(InfrastructureException):
    """Exception for external service errors."""
    
    def __init__(self, service: str, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        """
        Initialize external service exception.
        
        Args:
            service: Name of the external service
            message: Error message
            status_code: HTTP status code if applicable
            response_data: Response data from the service
        """
        super().__init__(f"External service '{service}' error: {message}")
        self.service = service
        self.status_code = status_code
        self.response_data = response_data
        self.error_code = "EXTERNAL_SERVICE_ERROR"


class RepositoryException(InfrastructureException):
    """Base exception for repository layer errors."""
    
    def __init__(self, message: str, repository: Optional[str] = None):
        """
        Initialize repository exception.
        
        Args:
            message: Error message
            repository: Name of the repository
        """
        super().__init__(message)
        self.repository = repository
        self.error_code = "REPOSITORY_ERROR"


class ProductCreationException(RepositoryException):
    """Exception for product creation failures."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="ProductRepository")
        self.error_code = "PRODUCT_CREATION_ERROR"


class ProductUpdateException(RepositoryException):
    """Exception for product update failures."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="ProductRepository")
        self.error_code = "PRODUCT_UPDATE_ERROR"


class ProductNotFoundException(RepositoryException):
    """Exception when product is not found."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="ProductRepository")
        self.error_code = "PRODUCT_NOT_FOUND"


class ProductRetrievalException(RepositoryException):
    """Exception for product retrieval failures."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="ProductRepository")
        self.error_code = "PRODUCT_RETRIEVAL_ERROR"


class ProductArchiveException(RepositoryException):
    """Exception for product archiving failures."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="ProductRepository")
        self.error_code = "PRODUCT_ARCHIVE_ERROR"


class MetafieldAssignmentException(RepositoryException):
    """Exception for metafield assignment failures."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="ProductRepository")
        self.error_code = "METAFIELD_ASSIGNMENT_ERROR"


class BulkOperationException(RepositoryException):
    """Exception for bulk operation failures."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = "BULK_OPERATION_ERROR"


class MetaobjectCreationException(RepositoryException):
    """Exception for metaobject creation failures."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="MetaobjectRepository")
        self.error_code = "METAOBJECT_CREATION_ERROR"


class MetaobjectRetrievalException(RepositoryException):
    """Exception for metaobject retrieval failures."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="MetaobjectRepository")
        self.error_code = "METAOBJECT_RETRIEVAL_ERROR"


class MetaobjectUpdateException(RepositoryException):
    """Exception for metaobject update failures."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="MetaobjectRepository")
        self.error_code = "METAOBJECT_UPDATE_ERROR"


class MetaobjectNotFoundException(RepositoryException):
    """Exception when metaobject is not found."""
    
    def __init__(self, message: str):
        super().__init__(message, repository="MetaobjectRepository")
        self.error_code = "METAOBJECT_NOT_FOUND"


class GraphQLQueryException(RepositoryException):
    """Exception for GraphQL query failures."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = "GRAPHQL_QUERY_ERROR"


class ApplicationException(Exception):
    """
    Base exception for application layer errors.
    
    This exception and its subclasses represent application-level
    errors such as workflow failures or use case errors.
    """
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 inner_exception: Optional[Exception] = None):
        """
        Initialize application exception.
        
        Args:
            message: Error message
            error_code: Optional error code
            inner_exception: The underlying exception
        """
        super().__init__(message)
        self.error_code = error_code
        self.inner_exception = inner_exception