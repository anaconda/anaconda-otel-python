#!/usr/bin/env python3
"""
Example 14: Counter Metrics

Demonstrates using counter metrics to track monotonically increasing values.
Counters are the most common metric type for tracking totals and rates.

WHEN TO USE COUNTERS:
- Track total number of events (requests, errors, logins)
- Count occurrences that only increase (never decrease)
- Calculate rates (requests per second, errors per minute)
- Track cumulative totals (bytes sent, items processed)

USE CASES:
- HTTP request counting
- Error and exception tracking
- User activity (logins, signups, actions)
- Business events (orders, payments, conversions)
- System events (cache hits/misses, database queries)

KEY CONCEPTS:
- Counters only increase (monotonic)
- Use increment_counter() to add to a counter
- Counters automatically start at 0
- Same counter name creates/reuses the same metric
- Attributes allow tracking different dimensions
"""

from anaconda.opentelemetry import (
    Configuration, 
    ResourceAttributes, 
    initialize_telemetry,
    increment_counter
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
    MetricAttributes,
    MetricValues,
    MetricDescriptions
)

# Test data constants
SERVICE_NAME = ServiceNameMetrics.METRICS_COUNTERS.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value


def main():
    print_header("Example 14: Counter Metrics", 
                 "Track monotonically increasing values with counters")
    
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
    print_info("✓ Telemetry initialized with metrics enabled")
    
    # Example 1: Basic counter increment
    print_section("2. Basic Counter Usage")
    print_info("\n  Example 1: Simple counter increment")
    increment_counter(CounterName.PAGE_VIEWS.value, by=1)
    print_code(f'increment_counter("{CounterName.PAGE_VIEWS.value}", by=1)')
    print_info("    → Increments page_views_total by 1")
    
    # Example 2: Increment by custom value
    print_info("\n  Example 2: Increment by custom value")
    increment_counter(CounterName.PAGE_VIEWS.value, by=5)
    print_code(f'increment_counter("{CounterName.PAGE_VIEWS.value}", by=5)')
    print_info("    → Increments page_views_total by 5")
    print_info("    → Total is now 6 (1 + 5)")
    
    # Example 3: Counter with attributes
    print_section("3. Counters with Attributes")
    print_info("\n  Example 3: Track API requests by endpoint")
    
    # Track different endpoints
    increment_counter(
        CounterName.API_REQUESTS.value, 
        by=1, 
        attributes=MetricAttributes.ENDPOINT_USERS.value
    )
    print_code(f'increment_counter("{CounterName.API_REQUESTS.value}", by=1, attributes={MetricAttributes.ENDPOINT_USERS.value})')
    
    increment_counter(
        CounterName.API_REQUESTS.value, 
        by=1, 
        attributes=MetricAttributes.ENDPOINT_ORDERS.value
    )
    print_code(f'increment_counter("{CounterName.API_REQUESTS.value}", by=1, attributes={MetricAttributes.ENDPOINT_ORDERS.value})')
    
    increment_counter(
        CounterName.API_REQUESTS.value, 
        by=1, 
        attributes=MetricAttributes.ENDPOINT_PRODUCTS.value
    )
    print_code(f'increment_counter("{CounterName.API_REQUESTS.value}", by=1, attributes={MetricAttributes.ENDPOINT_PRODUCTS.value})')
    
    print_info("    → Same metric name, different attributes")
    print_info("    → Backend can filter/aggregate by endpoint")
    
    # Example 4: Multiple counter types
    print_section("4. Different Counter Types")
    
    print_info("\n  Tracking cache operations:")
    increment_counter(CounterName.CACHE_HITS.value, by=10, attributes=MetricAttributes.CACHE_HIT.value)
    print_code(f'increment_counter("{CounterName.CACHE_HITS.value}", by=10, attributes=...)')
    
    increment_counter(CounterName.CACHE_MISSES.value, by=3, attributes=MetricAttributes.CACHE_MISS.value)
    print_code(f'increment_counter("{CounterName.CACHE_MISSES.value}", by=3, attributes=...)')
    
    print_info("\n  Tracking user activity:")
    increment_counter(CounterName.USER_LOGINS.value, by=5)
    print_code(f'increment_counter("{CounterName.USER_LOGINS.value}", by=5)')
    
    increment_counter(CounterName.USER_SIGNUPS.value, by=2)
    print_code(f'increment_counter("{CounterName.USER_SIGNUPS.value}", by=2)')
    
    print_info("\n  Tracking errors:")
    increment_counter(CounterName.ERRORS.value, by=1, attributes=MetricAttributes.STATUS_ERROR.value)
    print_code(f'increment_counter("{CounterName.ERRORS.value}", by=1, attributes=...)')
    
    # Example 5: Regional tracking
    print_section("5. Multi-Dimensional Tracking")
    print_info("\n  Track requests across different regions:")
    
    increment_counter(
        CounterName.REQUESTS_RECEIVED.value,
        by=MetricValues.INCREMENT_HUNDRED.value,
        attributes=MetricAttributes.REGION_US_EAST.value
    )
    print_code(f'increment_counter("{CounterName.REQUESTS_RECEIVED.value}", by=100, attributes={MetricAttributes.REGION_US_EAST.value})')
    
    increment_counter(
        CounterName.REQUESTS_RECEIVED.value,
        by=75,
        attributes=MetricAttributes.REGION_US_WEST.value
    )
    print_code(f'increment_counter("{CounterName.REQUESTS_RECEIVED.value}", by=75, attributes={MetricAttributes.REGION_US_WEST.value})')
    
    increment_counter(
        CounterName.REQUESTS_RECEIVED.value,
        by=50,
        attributes=MetricAttributes.REGION_EU_WEST.value
    )
    print_code(f'increment_counter("{CounterName.REQUESTS_RECEIVED.value}", by=50, attributes={MetricAttributes.REGION_EU_WEST.value})')
    
    increment_counter(CounterName.REQUESTS_COMPLETED.value, by=225)
    print_code(f'increment_counter("{CounterName.REQUESTS_COMPLETED.value}", by=225)')
    
    print_info("    → Total requests: 225 across all regions")
    print_info("    → All requests completed")
    
    # Example 6: Business metrics
    print_section("6. Business Metrics Tracking")
    print_info("\n  Track business events:")
    
    increment_counter(CounterName.ORDERS_CREATED.value, by=MetricValues.INCREMENT_TEN.value)
    print_code(f'increment_counter("{CounterName.ORDERS_CREATED.value}", by=10)')
    
    increment_counter(CounterName.PAYMENTS_PROCESSED.value, by=MetricValues.INCREMENT_TEN.value)
    print_code(f'increment_counter("{CounterName.PAYMENTS_PROCESSED.value}", by=10)')
    
    print_info("    → 10 orders created and paid")
    
    # Example 7: Network traffic
    print_section("7. Network Traffic Tracking")
    print_info("\n  Track data transfer:")
    
    increment_counter(CounterName.BYTES_SENT.value, by=1048576)
    print_code(f'increment_counter("{CounterName.BYTES_SENT.value}", by=1048576)')
    
    increment_counter(CounterName.BYTES_RECEIVED.value, by=524288)
    print_code(f'increment_counter("{CounterName.BYTES_RECEIVED.value}", by=524288)')
    
    print_info("    → Sent: 1 MB, Received: 512 KB")
    
    # Example 8: Floating-point counters (revenue tracking)
    print_section("8. Floating-Point Counters")
    print_info("\n  Track revenue with decimal precision:")
    print_info("  Note: Counters can use floating-point values for currency, percentages, etc.")
    
    increment_counter(CounterName.REVENUE_USD.value, by=MetricValues.REVENUE_SMALL.value)
    print_code(f'increment_counter("{CounterName.REVENUE_USD.value}", by={MetricValues.REVENUE_SMALL.value})')
    
    increment_counter(CounterName.REVENUE_USD.value, by=MetricValues.REVENUE_MEDIUM.value)
    print_code(f'increment_counter("{CounterName.REVENUE_USD.value}", by={MetricValues.REVENUE_MEDIUM.value})')
    
    increment_counter(CounterName.REVENUE_USD.value, by=MetricValues.REVENUE_LARGE.value)
    print_code(f'increment_counter("{CounterName.REVENUE_USD.value}", by={MetricValues.REVENUE_LARGE.value})')
    
    total_revenue = MetricValues.REVENUE_SMALL.value + MetricValues.REVENUE_MEDIUM.value + MetricValues.REVENUE_LARGE.value
    print_info(f"    → Total revenue: ${total_revenue:.2f} USD")
    print_info("    → Backend will store this as a floating-point counter (asDouble)")
    
    # Best practices
    print_section("9. Counter Best Practices")
    print_info(f"What is a counter? {MetricDescriptions.COUNTER.value}")
    print_info("Naming conventions:")
    print_info("  • Use descriptive names: 'api_requests_total' not 'count'")
    print_info("  • Add '_total' suffix for clarity")
    print_info("  • Use snake_case: 'page_views_total'")
    print_info("  • Be consistent across your application")
    print_info("\nWhen to use counters:")
    print_info("  ✓ Tracking totals (requests, errors, events)")
    print_info("  ✓ Calculating rates (per second, per minute)")
    print_info("  ✓ Cumulative values that only increase")
    print_info("  ✗ Values that can decrease (use up/down counter)")
    print_info("  ✗ Distributions of values (use histogram)")
    print_info("\nAttribute best practices:")
    print_info("  • Use attributes for dimensions (endpoint, region, status)")
    print_info("  • Keep cardinality reasonable (avoid unique IDs)")
    print_info("  • Use consistent attribute names")
    print_info("  • Group related attributes (http.*, db.*, cache.*)")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. initialize_telemetry(config, attrs, signal_types=['metrics'])")
    print_code("2. increment_counter(name, by=1)")
    print_code("3. increment_counter(name, by=5)")
    print_code("4. increment_counter(name, by=1, attributes={'key': 'value'})")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected counter metrics:")
    print_info(f"    - {CounterName.PAGE_VIEWS.value}: 6 (1 + 5)")
    print_info(f"    - {CounterName.API_REQUESTS.value}: 3 (with different endpoint attributes)")
    print_info(f"    - {CounterName.CACHE_HITS.value}: 10")
    print_info(f"    - {CounterName.CACHE_MISSES.value}: 3")
    print_info(f"    - {CounterName.USER_LOGINS.value}: 5")
    print_info(f"    - {CounterName.USER_SIGNUPS.value}: 2")
    print_info(f"    - {CounterName.ERRORS.value}: 1")
    print_info(f"    - {CounterName.REQUESTS_RECEIVED.value}: 225 (100 + 75 + 50 across regions)")
    print_info(f"    - {CounterName.REQUESTS_COMPLETED.value}: 225")
    print_info(f"    - {CounterName.ORDERS_CREATED.value}: 10")
    print_info(f"    - {CounterName.PAYMENTS_PROCESSED.value}: 10")
    print_info(f"    - {CounterName.BYTES_SENT.value}: 1048576 (1 MB)")
    print_info(f"    - {CounterName.BYTES_RECEIVED.value}: 524288 (512 KB)")
    print_info(f"    - {CounterName.REVENUE_USD.value}: 779.48 (floating-point counter)")
    print_info("  • All counters should have resource attributes")
    print_info("  • Counters with attributes should be filterable by those attributes")
    print_info("  • Floating-point counters stored as 'asDouble' in backend")
    
    print_footer("✓ Example 14 completed successfully!")


if __name__ == "__main__":
    main()
