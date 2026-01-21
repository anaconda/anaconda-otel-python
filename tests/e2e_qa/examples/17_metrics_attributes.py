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

from anaconda.opentelemetry import Configuration, ResourceAttributes
from utils import (
    load_environment,
    print_header,
    print_footer,
    print_info,
    print_section,
    print_environment_config,
    apply_signal_specific_endpoints,
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
    
    # Initialize SDK operations wrapper
    sdk = SdkOperations(
        endpoint=endpoint,
        service_name=SERVICE_NAME,
        service_version=SERVICE_VERSION
    )
    
    # Initialize with metrics enabled
    print_section("1. Initialize Telemetry")
    sdk.initialize(config, attrs, signal_types=['metrics'])
    
    # Example 1: HTTP status code tracking
    print_section("2. HTTP Status Code Tracking")
    print_info("Track requests by HTTP method and status:")
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=100, attributes={"http.method": "GET", "http.status_code": 200})
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=50, attributes={"http.method": "POST", "http.status_code": 201})
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=5, attributes={"http.method": "GET", "http.status_code": 500})
    
    print_info("Backend queries enabled:")
    print_info("  • Total requests: SUM(api_requests_total)")
    print_info("  • Success rate: COUNT(status_code=2xx) / COUNT(all)")
    print_info("  • Requests by method: GROUP BY http.method")
    
    # Example 2: Regional performance tracking
    print_section("3. Regional Performance Tracking")
    print_info("Track latency across different regions:")
    sdk.record_histogram_batch(HistogramName.REQUEST_DURATION_MS.value, [15.0, 18.0, 22.0, 16.0, 20.0], attributes=MetricAttributes.REGION_US_EAST.value)
    print_info("→ US East: 5 measurements (avg ~18ms)")
    
    sdk.record_histogram_batch(HistogramName.REQUEST_DURATION_MS.value, [45.0, 50.0, 48.0, 52.0, 47.0], attributes=MetricAttributes.REGION_US_WEST.value)
    print_info("→ US West: 5 measurements (avg ~48ms)")
    
    sdk.record_histogram_batch(HistogramName.REQUEST_DURATION_MS.value, [85.0, 90.0, 88.0, 92.0, 87.0], attributes=MetricAttributes.REGION_EU_WEST.value)
    print_info("→ EU West: 5 measurements (avg ~88ms)")
    
    print_info("Backend analysis:")
    print_info("  • Compare p95 latency by region")
    print_info("  • Identify slowest region")
    print_info("  • Track regional performance trends")
    
    # Example 3: User tier tracking
    print_section("4. User Tier Tracking")
    print_info("Track API usage by user tier:")
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=1000, attributes=MetricAttributes.USER_FREE.value)
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=500, attributes=MetricAttributes.USER_PREMIUM.value)
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=2000, attributes=MetricAttributes.USER_ENTERPRISE.value)
    
    print_info("Business insights:")
    print_info("  • Usage by tier: Free (1000), Premium (500), Enterprise (2000)")
    print_info("  • Revenue opportunity: Upgrade free users")
    print_info("  • Capacity planning: Enterprise users dominate")
    
    # Example 4: Database operation tracking
    print_section("5. Database Operation Tracking")
    print_info("Track database performance by operation and table:")
    sdk.record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, 12.5, attributes={"db.operation": "SELECT", "db.table": "users", "db.system": "postgresql"})
    sdk.record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, 45.0, attributes={"db.operation": "INSERT", "db.table": "orders", "db.system": "postgresql"})
    sdk.record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, 125.0, attributes={"db.operation": "UPDATE", "db.table": "products", "db.system": "postgresql"})
    
    print_info("Query optimization:")
    print_info("  • Identify slow tables")
    print_info("  • Compare operation types")
    print_info("  • Track query performance over time")
    
    # Example 5: Cache effectiveness
    print_section("6. Cache Effectiveness Tracking")
    print_info("Track cache hit/miss rates:")
    sdk.increment_counter(CounterName.CACHE_HITS.value, by=850, attributes=MetricAttributes.CACHE_HIT.value)
    sdk.increment_counter(CounterName.CACHE_MISSES.value, by=150, attributes=MetricAttributes.CACHE_MISS.value)
    sdk.increment_counter("cache_operations_total", by=1000, attributes=MetricAttributes.CACHE_SET.value)
    
    print_info("Cache metrics:")
    print_info("  • Hit rate: 850 / (850 + 150) = 85%")
    print_info("  • Miss rate: 150 / (850 + 150) = 15%")
    print_info("  • Set operations: 1000")
    
    # Example 6: Error tracking with status
    print_section("7. Error Status Tracking")
    print_info("Track errors by status type:")
    sdk.increment_counter(CounterName.ERRORS.value, by=5, attributes=MetricAttributes.STATUS_ERROR.value)
    sdk.increment_counter(CounterName.ERRORS.value, by=2, attributes=MetricAttributes.STATUS_TIMEOUT.value)
    
    print_info("Error breakdown:")
    print_info("  • General errors: 5")
    print_info("  • Timeout errors: 2")
    
    # Example 7: Metrics without attributes
    print_section("8. Metrics Without Attributes")
    print_info("Sometimes metrics don't need attributes:")
    sdk.increment_counter("simple_counter", by=100, attributes=MetricAttributes.EMPTY.value)
    print_info("→ Empty attributes for simple metrics")
    
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
