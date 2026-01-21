# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Test Data for Logging Examples

This module provides test data constants for logging examples including
log messages, log levels, and log attributes.
"""

from enum import Enum


class LogLevel(Enum):
    """Log level constants for examples."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogMessage(Enum):
    """Log message constants for examples."""
    # Basic logging messages
    BASIC_INFO = "This is a basic info log message"
    BASIC_WARNING = "This is a warning log message"
    BASIC_ERROR = "This is an error log message"
    BASIC_DEBUG = "This is a debug log message"
    BASIC_CRITICAL = "This is a critical log message"
    
    # Structured logging messages
    USER_LOGIN = "User logged in successfully"
    USER_LOGOUT = "User logged out"
    DATABASE_QUERY = "Database query executed"
    API_REQUEST = "API request received"
    CACHE_HIT = "Cache hit for key"
    CACHE_MISS = "Cache miss for key"
    
    # Error scenarios
    CONNECTION_FAILED = "Failed to connect to database"
    TIMEOUT_ERROR = "Request timeout exceeded"
    VALIDATION_ERROR = "Input validation failed"
    PERMISSION_DENIED = "Permission denied for operation"
    
    # Performance logging
    SLOW_QUERY = "Slow database query detected"
    HIGH_MEMORY = "High memory usage detected"
    RATE_LIMIT = "Rate limit exceeded"


class LogAttributes(Enum):
    """Log attribute constants for examples."""
    # User-related attributes
    USER_BASIC = {"user.id": "user123", "user.name": "john_doe"}
    USER_WITH_EMAIL = {"user.id": "user456", "user.name": "jane_smith", "user.email": "jane@example.com"}
    USER_WITH_ROLE = {"user.id": "admin001", "user.name": "admin", "user.role": "administrator"}
    
    # Request-related attributes
    HTTP_REQUEST = {"http.method": "GET", "http.url": "/api/users", "http.status_code": 200}
    HTTP_POST = {"http.method": "POST", "http.url": "/api/data", "http.status_code": 201}
    HTTP_ERROR = {"http.method": "GET", "http.url": "/api/error", "http.status_code": 500}
    
    # Database-related attributes
    DB_QUERY = {"db.system": "postgresql", "db.operation": "SELECT", "db.table": "users"}
    DB_INSERT = {"db.system": "postgresql", "db.operation": "INSERT", "db.table": "orders"}
    DB_SLOW_QUERY = {"db.system": "postgresql", "db.operation": "SELECT", "db.query_time_ms": 5000}
    
    # Performance attributes
    PERFORMANCE = {"duration_ms": 150, "memory_mb": 256}
    SLOW_OPERATION = {"duration_ms": 3000, "operation": "data_processing"}
    
    # Error attributes
    ERROR_CONTEXT = {"error.type": "ConnectionError", "error.message": "Connection refused"}
    VALIDATION_ERROR = {"error.type": "ValidationError", "field": "email", "reason": "invalid_format"}
    
    # Cache attributes
    CACHE_INFO = {"cache.key": "user:123", "cache.hit": True}
    CACHE_MISS_INFO = {"cache.key": "product:456", "cache.hit": False}
    
    # Empty attributes
    EMPTY = {}


class LoggerName(Enum):
    """Logger name constants for examples."""
    APP_LOGGER = "app.main"
    API_LOGGER = "app.api"
    DATABASE_LOGGER = "app.database"
    AUTH_LOGGER = "app.auth"
    CACHE_LOGGER = "app.cache"
    CUSTOM_LOGGER = "my_custom_logger"
    MULTIPLE_LOGGER_1 = "app.service1"
    MULTIPLE_LOGGER_2 = "app.service2"
    MULTIPLE_LOGGER_3 = "app.service3"


class ServiceNameLogging(Enum):
    """Service name constants for logging examples."""
    LOGGING_BASIC = "example-08-logging-basic"
    LOGGING_LEVELS = "example-09-logging-levels"
    LOGGING_STRUCTURED = "example-10-logging-structured"
    LOGGING_MULTIPLE = "example-11-logging-multiple"
    LOGGING_INTEGRATION = "example-12-logging-integration"
    LOGGING_FLUSH = "example-13-logging-flush"
