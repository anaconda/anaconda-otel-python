#!/usr/bin/env python3
"""
Example 17: Metrics with Attributes

Demonstrates advanced usage of attributes with metrics for multi-dimensional
analysis. Shows how to use attributes effectively for filtering and aggregation.

WHEN TO USE ATTRIBUTES:
- Track metrics across multiple dimensions (region, environment, version)
- Enable filtering in backend queries
- Support aggregation and grouping
- Correlate metrics with context
- Analyze metrics by specific criteria

USE CASES:
- Multi-region deployments (track by region)
- A/B testing (track by variant)
- User segmentation (track by user type)
- API versioning (track by version)
- Error categorization (track by error type)
- Performance by endpoint (track by URL)

KEY CONCEPTS:
- Attributes add dimensions to metrics
- Same metric name with different attributes creates separate series
- Keep cardinality reasonable (avoid unique IDs)
- Use consistent attribute naming
- Attributes enable powerful backend queries
"""

from anaconda.opentelemetry import (
    Configuration, 
    ResourceAttributes, 
    initialize_telemetry,
    increment_counter,
    record_histogram
)
from utils import (
    EndpointType,
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_code,
    print_section,
    print_environment_config,
    apply_signal_specific_endpoints
)
from test_data import (
    ServiceVersion,
    ServiceNameMetrics,
    CounterName,
    HistogramName,
    MetricAttributes,
    MetricValues
)

# Test data constants
SERVICE_NAME = ServiceNameMetrics.METRICS_ATTRIBUTES.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value


def main():
    print_header("Example 17: Metrics with Attributes", 
                 "Multi-dimensional metrics analysis with attributes")
    
    # Load environment
    _, endpoint, use_console, endpoints = load_environment()
    print_environment_config(endpoint, use_console)
    
    # Create configuration
    config = Configuration(default_endpoint=endpoint)
    apply_signal_specific_endpoints(config, endpoints)
    if use_console:
        config.set_console_exporter(use_console=True)
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with metrics enabled
    print_section("1. Initialize Telemetry")
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics'])")
    print_info("✓ Telemetry initialized")
    
    # Example 1: HTTP status code tracking
    print_section("2. HTTP Status Code Tracking")
    print_info("\n  Track requests by HTTP method and status:")
    
    # Successful GET requests
    increment_counter(
        CounterName.API_REQUESTS.value,
        by=100,
        attributes={"http.method": "GET", "http.status_code": 200}
    )
    print_code('increment_counter("api_requests_total", by=100, attributes={"http.method": "GET", "http.status_code": 200})')
    
    # Successful POST requests
    increment_counter(
        CounterName.API_REQUESTS.value,
        by=50,
        attributes={"http.method": "POST", "http.status_code": 201}
    )
    print_code('increment_counter("api_requests_total", by=50, attributes={"http.method": "POST", "http.status_code": 201})')
    
    # Error requests
    increment_counter(
        CounterName.API_REQUESTS.value,
        by=5,
        attributes={"http.method": "GET", "http.status_code": 500}
    )
    print_code('increment_counter("api_requests_total", by=5, attributes={"http.method": "GET", "http.status_code": 500})')
    
    print_info("\n  Backend queries enabled:")
    print_info("    • Total requests: SUM(api_requests_total)")
    print_info("    • Success rate: COUNT(status_code=2xx) / COUNT(all)")
    print_info("    • Requests by method: GROUP BY http.method")
    
    # Example 2: Regional performance tracking
    print_section("3. Regional Performance Tracking")
    print_info("\n  Track latency across different regions:")
    
    # US East - fast responses
    for duration in [15.0, 18.0, 22.0, 16.0, 20.0]:
        record_histogram(
            HistogramName.REQUEST_DURATION_MS.value,
            duration,
            attributes=MetricAttributes.REGION_US_EAST.value
        )
    print_code('record_histogram("request_duration_ms", duration, attributes=REGION_US_EAST)')
    print_info("    → US East: 5 measurements (avg ~18ms)")
    
    # US West - moderate responses
    for duration in [45.0, 50.0, 48.0, 52.0, 47.0]:
        record_histogram(
            HistogramName.REQUEST_DURATION_MS.value,
            duration,
            attributes=MetricAttributes.REGION_US_WEST.value
        )
    print_code('record_histogram("request_duration_ms", duration, attributes=REGION_US_WEST)')
    print_info("    → US West: 5 measurements (avg ~48ms)")
    
    # EU West - slower responses
    for duration in [85.0, 90.0, 88.0, 92.0, 87.0]:
        record_histogram(
            HistogramName.REQUEST_DURATION_MS.value,
            duration,
            attributes=MetricAttributes.REGION_EU_WEST.value
        )
    print_code('record_histogram("request_duration_ms", duration, attributes=REGION_EU_WEST)')
    print_info("    → EU West: 5 measurements (avg ~88ms)")
    
    print_info("\n  Backend analysis:")
    print_info("    • Compare p95 latency by region")
    print_info("    • Identify slowest region")
    print_info("    • Track regional performance trends")
    
    # Example 3: User tier tracking
    print_section("4. User Tier Tracking")
    print_info("\n  Track API usage by user tier:")
    
    # Free tier users
    increment_counter(
        CounterName.API_REQUESTS.value,
        by=1000,
        attributes=MetricAttributes.USER_FREE.value
    )
    print_code('increment_counter("api_requests_total", by=1000, attributes=USER_FREE)')
    
    # Premium users
    increment_counter(
        CounterName.API_REQUESTS.value,
        by=500,
        attributes=MetricAttributes.USER_PREMIUM.value
    )
    print_code('increment_counter("api_requests_total", by=500, attributes=USER_PREMIUM)')
    
    # Enterprise users
    increment_counter(
        CounterName.API_REQUESTS.value,
        by=2000,
        attributes=MetricAttributes.USER_ENTERPRISE.value
    )
    print_code('increment_counter("api_requests_total", by=2000, attributes=USER_ENTERPRISE)')
    
    print_info("\n  Business insights:")
    print_info("    • Usage by tier: Free (1000), Premium (500), Enterprise (2000)")
    print_info("    • Revenue opportunity: Upgrade free users")
    print_info("    • Capacity planning: Enterprise users dominate")
    
    # Example 4: Database operation tracking
    print_section("5. Database Operation Tracking")
    print_info("\n  Track database performance by operation and table:")
    
    # User table operations
    record_histogram(
        HistogramName.DATABASE_QUERY_DURATION_MS.value,
        12.5,
        attributes={"db.operation": "SELECT", "db.table": "users", "db.system": "postgresql"}
    )
    print_code('record_histogram("database_query_duration_ms", 12.5, attributes={"db.operation": "SELECT", "db.table": "users", ...})')
    
    # Orders table operations
    record_histogram(
        HistogramName.DATABASE_QUERY_DURATION_MS.value,
        45.0,
        attributes={"db.operation": "INSERT", "db.table": "orders", "db.system": "postgresql"}
    )
    print_code('record_histogram("database_query_duration_ms", 45.0, attributes={"db.operation": "INSERT", "db.table": "orders", ...})')
    
    # Products table operations
    record_histogram(
        HistogramName.DATABASE_QUERY_DURATION_MS.value,
        125.0,
        attributes={"db.operation": "UPDATE", "db.table": "products", "db.system": "postgresql"}
    )
    print_code('record_histogram("database_query_duration_ms", 125.0, attributes={"db.operation": "UPDATE", "db.table": "products", ...})')
    
    print_info("\n  Query optimization:")
    print_info("    • Identify slow tables")
    print_info("    • Compare operation types")
    print_info("    • Track query performance over time")
    
    # Example 5: Cache effectiveness
    print_section("6. Cache Effectiveness Tracking")
    print_info("\n  Track cache hit/miss rates:")
    
    # Cache hits
    increment_counter(
        CounterName.CACHE_HITS.value,
        by=850,
        attributes=MetricAttributes.CACHE_HIT.value
    )
    print_code('increment_counter("cache_hits_total", by=850, attributes=CACHE_HIT)')
    
    # Cache misses
    increment_counter(
        CounterName.CACHE_MISSES.value,
        by=150,
        attributes=MetricAttributes.CACHE_MISS.value
    )
    print_code('increment_counter("cache_misses_total", by=150, attributes=CACHE_MISS)')
    
    # Cache set operations
    increment_counter(
        "cache_operations_total",
        by=1000,
        attributes=MetricAttributes.CACHE_SET.value
    )
    print_code('increment_counter("cache_operations_total", by=1000, attributes=CACHE_SET)')
    
    print_info("\n  Cache metrics:")
    print_info("    • Hit rate: 850 / (850 + 150) = 85%")
    print_info("    • Miss rate: 150 / (850 + 150) = 15%")
    print_info("    • Set operations: 1000")
    
    # Example 6: Error tracking with status
    print_section("7. Error Status Tracking")
    print_info("\n  Track errors by status type:")
    
    increment_counter(
        CounterName.ERRORS.value,
        by=MetricValues.INCREMENT_FIVE.value,
        attributes=MetricAttributes.STATUS_ERROR.value
    )
    print_code('increment_counter("errors_total", by=5, attributes=STATUS_ERROR)')
    
    increment_counter(
        CounterName.ERRORS.value,
        by=2,
        attributes=MetricAttributes.STATUS_TIMEOUT.value
    )
    print_code('increment_counter("errors_total", by=2, attributes=STATUS_TIMEOUT)')
    
    print_info("\n  Error breakdown:")
    print_info("    • General errors: 5")
    print_info("    • Timeout errors: 2")
    
    # Example 7: Metrics without attributes
    print_section("8. Metrics Without Attributes")
    print_info("\n  Sometimes metrics don't need attributes:")
    
    increment_counter(
        "simple_counter",
        by=MetricValues.INCREMENT_HUNDRED.value,
        attributes=MetricAttributes.EMPTY.value
    )
    print_code('increment_counter("simple_counter", by=100, attributes=EMPTY)')
    print_info("    → Empty attributes for simple metrics")
    
    # Best practices
    print_section("9. Attribute Best Practices")
    print_info("Naming conventions:")
    print_info("  • Use dot notation: 'http.method', 'db.table', 'user.type'")
    print_info("  • Group related attributes: 'http.*', 'db.*', 'user.*'")
    print_info("  • Be consistent across metrics")
    print_info("  • Use lowercase with underscores: 'error_type' not 'ErrorType'")
    print_info("\nCardinality management:")
    print_info("  ✓ Low cardinality: http.method (GET, POST, PUT, DELETE)")
    print_info("  ✓ Low cardinality: region (us-east, us-west, eu-west)")
    print_info("  ✓ Low cardinality: user.type (free, premium, enterprise)")
    print_info("  ✗ High cardinality: user.id (unique per user)")
    print_info("  ✗ High cardinality: request.id (unique per request)")
    print_info("  ✗ High cardinality: timestamp (unique per second)")
    print_info("\nAttribute selection:")
    print_info("  • Choose attributes that enable useful queries")
    print_info("  • Limit to 5-10 attributes per metric")
    print_info("  • Avoid attributes that change frequently")
    print_info("  • Use attributes for dimensions, not unique identifiers")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. increment_counter(name, by=value, attributes={'key': 'value'})")
    print_code("2. record_histogram(name, value, attributes={'key': 'value'})")
    print_code("3. Multiple attributes: attributes={'key1': 'val1', 'key2': 'val2'}")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected metrics with attributes:")
    print_info("    - api_requests_total: Multiple series by http.method and http.status_code")
    print_info("    - request_duration_ms: 3 series by region (15 total measurements)")
    print_info("    - api_requests_total: 3 series by user.type (3500 total)")
    print_info("    - database_query_duration_ms: 3 measurements with db.* attributes")
    print_info("    - cache_hits_total: 850")
    print_info("    - cache_misses_total: 150")
    print_info("    - cache_operations_total: 1000 (with CACHE_SET attributes)")
    print_info("    - errors_total: 7 (5 STATUS_ERROR + 2 STATUS_TIMEOUT)")
    print_info("    - simple_counter: 100 (with EMPTY attributes)")
    print_info("  • All metrics should be filterable by their attributes")
    
    print_footer("✓ Example 17 completed successfully!")


if __name__ == "__main__":
    main()
