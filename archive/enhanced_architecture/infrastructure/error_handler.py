"""
Centralized error handling system for the Shopify Bulk Importer.

This module provides consistent error handling, logging, and reporting
across all layers of the application.
"""

from typing import Dict, Any, Optional, List, Type
import logging
import traceback
from datetime import datetime
from infrastructure.exceptions import *


class ErrorContext:
    """
    Context information for error handling.
    
    This class captures contextual information about where and when
    errors occur to aid in debugging and monitoring.
    """
    
    def __init__(self, operation: str, user_id: Optional[str] = None, 
                 session_id: Optional[str] = None):
        """
        Initialize error context.
        
        Args:
            operation: The operation being performed
            user_id: Optional user identifier
            session_id: Optional session identifier
        """
        self.operation = operation
        self.user_id = user_id
        self.session_id = session_id
        self.timestamp = datetime.utcnow()
        self.additional_data: Dict[str, Any] = {}
    
    def add_data(self, key: str, value: Any) -> None:
        """
        Add additional context data.
        
        Args:
            key: Data key
            value: Data value
        """
        self.additional_data[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert context to dictionary.
        
        Returns:
            Dictionary representation of the context
        """
        return {
            "operation": self.operation,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "additional_data": self.additional_data
        }


class ErrorHandler:
    """
    Centralized error handling system.
    
    This class provides consistent error processing, logging, and
    response formatting across the entire application.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the error handler.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self._error_counts: Dict[str, int] = {}
    
    def handle_error(self, exception: Exception, 
                    context: Optional[ErrorContext] = None) -> Dict[str, Any]:
        """
        Handle and process errors.
        
        Args:
            exception: The exception that occurred
            context: Optional context information
            
        Returns:
            Standardized error response dictionary
        """
        error_response = self._create_error_response(exception, context)
        self._log_error(exception, context, error_response)
        self._track_error_statistics(exception)
        
        return error_response
    
    def _create_error_response(self, exception: Exception, 
                              context: Optional[ErrorContext]) -> Dict[str, Any]:
        """
        Create standardized error response.
        
        Args:
            exception: The exception that occurred
            context: Optional context information
            
        Returns:
            Standardized error response dictionary
        """
        response = {
            "success": False,
            "error_type": type(exception).__name__,
            "message": str(exception),
            "timestamp": datetime.utcnow().isoformat(),
            "trace_id": self._generate_trace_id()
        }
        
        # Add specific error information based on exception type
        if isinstance(exception, ValidationException):
            response.update({
                "error_code": exception.error_code,
                "field": exception.field,
                "value": exception.value,
                "severity": "warning"
            })
        
        elif isinstance(exception, BusinessRuleException):
            response.update({
                "error_code": exception.error_code,
                "rule": exception.rule,
                "context": exception.context,
                "severity": "warning"
            })
        
        elif isinstance(exception, ExternalServiceException):
            response.update({
                "error_code": exception.error_code,
                "service": exception.service,
                "status_code": exception.status_code,
                "external_response": exception.response_data,
                "severity": "error"
            })
        
        elif isinstance(exception, RepositoryException):
            response.update({
                "error_code": exception.error_code,
                "repository": exception.repository,
                "severity": "error"
            })
        
        elif isinstance(exception, DomainException):
            response.update({
                "error_code": exception.error_code,
                "context": exception.context,
                "severity": "warning"
            })
        
        elif isinstance(exception, InfrastructureException):
            response.update({
                "error_code": exception.error_code,
                "original_exception": str(exception.original_exception) if exception.original_exception else None,
                "severity": "error"
            })
        
        elif isinstance(exception, ApplicationException):
            response.update({
                "error_code": exception.error_code,
                "inner_exception": str(exception.inner_exception) if exception.inner_exception else None,
                "severity": "error"
            })
        
        else:
            # Unknown exception type
            response.update({
                "error_code": "UNKNOWN_ERROR",
                "severity": "error"
            })
        
        # Add context information
        if context:
            response["context"] = context.to_dict()
        
        # Add stack trace for debugging (only in development)
        response["stack_trace"] = traceback.format_exc()
        
        return response
    
    def _log_error(self, exception: Exception, context: Optional[ErrorContext], 
                   error_response: Dict[str, Any]) -> None:
        """
        Log error with appropriate level.
        
        Args:
            exception: The exception that occurred
            context: Optional context information
            error_response: The error response dictionary
        """
        log_level = self._determine_log_level(exception)
        operation = context.operation if context else "unknown"
        
        log_message = f"Error in operation '{operation}': {str(exception)}"
        
        # Create log extra data
        extra = {
            "error_response": error_response,
            "exception_type": type(exception).__name__,
            "trace_id": error_response.get("trace_id")
        }
        
        if context:
            extra.update({
                "user_id": context.user_id,
                "session_id": context.session_id,
                "additional_data": context.additional_data
            })
        
        # Log with appropriate level
        if log_level == logging.ERROR:
            self.logger.error(log_message, exc_info=exception, extra=extra)
        elif log_level == logging.WARNING:
            self.logger.warning(log_message, extra=extra)
        else:
            self.logger.info(log_message, extra=extra)
    
    def _determine_log_level(self, exception: Exception) -> int:
        """
        Determine appropriate log level for exception.
        
        Args:
            exception: The exception to categorize
            
        Returns:
            Logging level constant
        """
        # Critical system errors
        if isinstance(exception, (ExternalServiceException, InfrastructureException)):
            return logging.ERROR
        
        # Repository errors
        elif isinstance(exception, RepositoryException):
            return logging.ERROR
        
        # Application errors
        elif isinstance(exception, ApplicationException):
            return logging.ERROR
        
        # Business rule violations
        elif isinstance(exception, BusinessRuleException):
            return logging.WARNING
        
        # Validation errors
        elif isinstance(exception, ValidationException):
            return logging.INFO
        
        # Domain errors
        elif isinstance(exception, DomainException):
            return logging.WARNING
        
        # Unknown errors
        else:
            return logging.ERROR
    
    def _track_error_statistics(self, exception: Exception) -> None:
        """
        Track error statistics for monitoring.
        
        Args:
            exception: The exception that occurred
        """
        error_type = type(exception).__name__
        self._error_counts[error_type] = self._error_counts.get(error_type, 0) + 1
    
    def _generate_trace_id(self) -> str:
        """
        Generate unique trace ID for error tracking.
        
        Returns:
            Unique trace identifier
        """
        import uuid
        return str(uuid.uuid4())[:8]
    
    def get_error_statistics(self) -> Dict[str, int]:
        """
        Get error statistics.
        
        Returns:
            Dictionary of error counts by type
        """
        return self._error_counts.copy()
    
    def reset_statistics(self) -> None:
        """Reset error statistics."""
        self._error_counts.clear()


class ErrorHandlerMiddleware:
    """
    Middleware for automatic error handling in Streamlit applications.
    
    This class provides decorators for automatic error handling.
    """
    
    def __init__(self, error_handler: ErrorHandler):
        """
        Initialize middleware.
        
        Args:
            error_handler: The error handler instance
        """
        self.error_handler = error_handler
    
    def handle_errors(self, operation_name: str, show_user_message: bool = True):
        """
        Decorator for automatic error handling.
        
        Args:
            operation_name: Name of the operation being performed
            show_user_message: Whether to show user-friendly messages
            
        Returns:
            Decorator function
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                context = ErrorContext(operation_name)
                
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_response = self.error_handler.handle_error(e, context)
                    
                    if show_user_message:
                        import streamlit as st
                        severity = error_response.get("severity", "error")
                        
                        if severity == "error":
                            st.error(f"Error: {error_response['message']}")
                        elif severity == "warning":
                            st.warning(f"Warning: {error_response['message']}")
                        else:
                            st.info(f"Info: {error_response['message']}")
                    
                    return {"success": False, "error": error_response}
            
            return wrapper
        return decorator


# Global error handler instance
_error_handler: Optional[ErrorHandler] = None


def get_error_handler() -> ErrorHandler:
    """
    Get the global error handler instance.
    
    Returns:
        The global error handler
    """
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler


def handle_error(exception: Exception, context: Optional[ErrorContext] = None) -> Dict[str, Any]:
    """
    Convenience function for handling errors.
    
    Args:
        exception: The exception that occurred
        context: Optional context information
        
    Returns:
        Error response dictionary
    """
    return get_error_handler().handle_error(exception, context)