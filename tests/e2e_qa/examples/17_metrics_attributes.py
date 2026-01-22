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

from utils import (
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_section,
    print_environment_config,
    SdkOperations,
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
    
    # Initialize SDK operations wrapper
    sdk = SdkOperations(
        endpoint=endpoint,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Create configuration
    config = sdk.create_configuration(endpoint=endpoint, use_console=use_console)
    sdk.apply_signal_specific_endpoints(config, endpoints)
    
    # Create attributes
    attrs = sdk.create_attributes(
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with metrics enabled
    print_section("1. Initialize Telemetry")
    sdk.initialize(config, attrs, signal_types=['metrics'])
    
    # Example 1: HTTP status code tracking
    print_section("2. HTTP Status Code Tracking")
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=100, attributes={"http.method": "GET", "http.status_code": 200})
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=50, attributes={"http.method": "POST", "http.status_code": 201})
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=5, attributes={"http.method": "GET", "http.status_code": 500})
    print_info("-> Attributes enable backend queries: totals, success rates, grouping by method")
    
    # Example 2: Regional performance tracking
    print_section("3. Regional Performance Tracking")
    sdk.record_histogram_batch(HistogramName.REQUEST_DURATION_MS.value, [15.0, 18.0, 22.0, 16.0, 20.0], attributes=MetricAttributes.REGION_US_EAST.value)
    sdk.record_histogram_batch(HistogramName.REQUEST_DURATION_MS.value, [45.0, 50.0, 48.0, 52.0, 47.0], attributes=MetricAttributes.REGION_US_WEST.value)
    sdk.record_histogram_batch(HistogramName.REQUEST_DURATION_MS.value, [85.0, 90.0, 88.0, 92.0, 87.0], attributes=MetricAttributes.REGION_EU_WEST.value)
    print_info("-> Region attributes enable performance comparison and trend analysis")
    
    # Example 3: User tier tracking
    print_section("4. User Tier Tracking")
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=1000, attributes=MetricAttributes.USER_FREE.value)
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=500, attributes=MetricAttributes.USER_PREMIUM.value)
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=2000, attributes=MetricAttributes.USER_ENTERPRISE.value)
    print_info("-> User tier attributes enable business insights and capacity planning")
    
    # Example 4: Database operation tracking
    print_section("5. Database Operation Tracking")
    sdk.record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, 12.5, attributes={"db.operation": "SELECT", "db.table": "users", "db.system": "postgresql"})
    sdk.record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, 45.0, attributes={"db.operation": "INSERT", "db.table": "orders", "db.system": "postgresql"})
    sdk.record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, 125.0, attributes={"db.operation": "UPDATE", "db.table": "products", "db.system": "postgresql"})
    print_info("-> Multiple attributes enable detailed query optimization analysis")
    
    # Example 5: Cache effectiveness
    print_section("6. Cache Effectiveness Tracking")
    sdk.increment_counter(CounterName.CACHE_HITS.value, by=850, attributes=MetricAttributes.CACHE_HIT.value)
    sdk.increment_counter(CounterName.CACHE_MISSES.value, by=150, attributes=MetricAttributes.CACHE_MISS.value)
    sdk.increment_counter("cache_operations_total", by=1000, attributes=MetricAttributes.CACHE_SET.value)
    
    # Example 6: Error tracking with status
    print_section("7. Error Status Tracking")
    sdk.increment_counter(CounterName.ERRORS.value, by=5, attributes=MetricAttributes.STATUS_ERROR.value)
    sdk.increment_counter(CounterName.ERRORS.value, by=2, attributes=MetricAttributes.STATUS_TIMEOUT.value)
    
    # Example 7: Metrics without attributes
    print_section("8. Metrics Without Attributes")
    sdk.increment_counter("simple_counter", by=100, attributes=MetricAttributes.EMPTY.value)
    print_info("-> Attributes are optional - use them when multi-dimensional analysis is needed")
    
    print_footer("[OK] Example 17 completed successfully!")


if __name__ == "__main__":
    main()
