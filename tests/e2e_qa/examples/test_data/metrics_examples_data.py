# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Test Data for Metrics Examples

This module provides test data constants for metrics examples including
metric names, values, and attributes.
"""

from enum import Enum


class ServiceNameMetrics(Enum):
    """Service name constants for metrics examples."""
    METRICS_COUNTERS = "example-14-metrics-counters"
    METRICS_HISTOGRAM = "example-15-metrics-histogram"
    METRICS_UPDOWN = "example-16-metrics-updown"
    METRICS_ATTRIBUTES = "example-17-metrics-attributes"
    METRICS_PATTERNS = "example-18-metrics-patterns"
    METRICS_FLUSH = "example-19-metrics-flush"


class CounterName(Enum):
    """Counter metric name constants."""
    # Basic counters
    PAGE_VIEWS = "page_views_total"
    API_REQUESTS = "api_requests_total"
    ERRORS = "errors_total"
    CACHE_HITS = "cache_hits_total"
    CACHE_MISSES = "cache_misses_total"
    
    # Feature-specific counters
    USER_LOGINS = "user_logins_total"
    USER_SIGNUPS = "user_signups_total"
    ORDERS_CREATED = "orders_created_total"
    PAYMENTS_PROCESSED = "payments_processed_total"
    
    # System counters
    REQUESTS_RECEIVED = "requests_received_total"
    REQUESTS_COMPLETED = "requests_completed_total"
    BYTES_SENT = "bytes_sent_total"
    BYTES_RECEIVED = "bytes_received_total"
    
    # Floating-point counters
    REVENUE_USD = "revenue_usd_total"


class UpDownCounterName(Enum):
    """Up/down counter metric name constants."""
    ACTIVE_CONNECTIONS = "active_connections"
    ACTIVE_USERS = "active_users"
    QUEUE_SIZE = "queue_size"
    MEMORY_USAGE_MB = "memory_usage_mb"
    DISK_USAGE_GB = "disk_usage_gb"
    CONCURRENT_REQUESTS = "concurrent_requests"
    ACTIVE_SESSIONS = "active_sessions"
    ITEMS_IN_CART = "items_in_cart"


class HistogramName(Enum):
    """Histogram metric name constants."""
    # Latency histograms
    REQUEST_DURATION_MS = "request_duration_ms"
    DATABASE_QUERY_DURATION_MS = "database_query_duration_ms"
    API_RESPONSE_TIME_MS = "api_response_time_ms"
    CACHE_LOOKUP_DURATION_MS = "cache_lookup_duration_ms"
    
    # Size histograms
    REQUEST_SIZE_BYTES = "request_size_bytes"
    RESPONSE_SIZE_BYTES = "response_size_bytes"
    FILE_SIZE_BYTES = "file_size_bytes"
    
    # Business metrics
    ORDER_VALUE_USD = "order_value_usd"
    CART_VALUE_USD = "cart_value_usd"
    TRANSACTION_AMOUNT_USD = "transaction_amount_usd"


class MetricAttributes(Enum):
    """Metric attribute constants."""
    # HTTP attributes
    HTTP_GET = {"http.method": "GET", "http.status_code": 200}
    HTTP_POST = {"http.method": "POST", "http.status_code": 201}
    HTTP_ERROR = {"http.method": "GET", "http.status_code": 500}
    
    # Endpoint attributes
    ENDPOINT_USERS = {"endpoint": "/api/users", "method": "GET"}
    ENDPOINT_ORDERS = {"endpoint": "/api/orders", "method": "POST"}
    ENDPOINT_PRODUCTS = {"endpoint": "/api/products", "method": "GET"}
    
    # Database attributes
    DB_SELECT = {"db.operation": "SELECT", "db.table": "users"}
    DB_INSERT = {"db.operation": "INSERT", "db.table": "orders"}
    DB_UPDATE = {"db.operation": "UPDATE", "db.table": "products"}
    
    # Cache attributes
    CACHE_HIT = {"cache.operation": "get", "cache.result": "hit"}
    CACHE_MISS = {"cache.operation": "get", "cache.result": "miss"}
    CACHE_SET = {"cache.operation": "set"}
    
    # Region attributes
    REGION_US_EAST = {"region": "us-east-1", "datacenter": "dc1"}
    REGION_US_WEST = {"region": "us-west-2", "datacenter": "dc2"}
    REGION_EU_WEST = {"region": "eu-west-1", "datacenter": "dc3"}
    
    # Status attributes
    STATUS_SUCCESS = {"status": "success"}
    STATUS_ERROR = {"status": "error"}
    STATUS_TIMEOUT = {"status": "timeout"}
    
    # User type attributes
    USER_FREE = {"user.type": "free", "user.tier": "basic"}
    USER_PREMIUM = {"user.type": "premium", "user.tier": "pro"}
    USER_ENTERPRISE = {"user.type": "enterprise", "user.tier": "enterprise"}
    
    # Empty attributes
    EMPTY = {}


class MetricValues(Enum):
    """Common metric value constants."""
    # Counter increments
    INCREMENT_ONE = 1
    INCREMENT_FIVE = 5
    INCREMENT_TEN = 10
    INCREMENT_HUNDRED = 100
    
    # Counter increments (floating-point)
    REVENUE_SMALL = 29.99
    REVENUE_MEDIUM = 149.50
    REVENUE_LARGE = 599.99
    
    # Histogram values (durations in ms)
    FAST_RESPONSE = 15.5
    NORMAL_RESPONSE = 125.0
    SLOW_RESPONSE = 850.0
    VERY_SLOW_RESPONSE = 3000.0
    
    # Histogram values (sizes in bytes)
    SMALL_SIZE = 1024
    MEDIUM_SIZE = 10240
    LARGE_SIZE = 102400
    
    # Histogram values (business metrics in USD)
    SMALL_ORDER = 9.99
    MEDIUM_ORDER = 49.99
    LARGE_ORDER = 199.99
    
    # Up/down counter changes
    INCREASE_ONE = 1
    INCREASE_FIVE = 5
    DECREASE_ONE = 1
    DECREASE_FIVE = 5


class MetricDescriptions(Enum):
    """Metric description constants for documentation."""
    COUNTER = "Monotonically increasing counter (only goes up)"
    UPDOWN_COUNTER = "Counter that can increase or decrease"
    HISTOGRAM = "Records distribution of values over time"
