#!/usr/bin/env python3
"""
Example 14: Counter Metrics

Demonstrates using counter metrics to track monotonically increasing values.

WHEN TO USE COUNTERS:
- Track total number of events (requests, errors, logins)
- Count occurrences that only increase (never decrease)
- Calculate rates (requests per second, errors per minute)
- Track cumulative totals (bytes sent, items processed)
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
    
    # Example 1: Basic counter increment
    print_section("2. Basic Counter Usage")
    sdk.increment_counter(CounterName.PAGE_VIEWS.value, by=1)
    sdk.increment_counter(CounterName.PAGE_VIEWS.value, by=5)
    print_info("-> Counters accumulate across multiple calls")
    
    # Example 3: Counter with attributes
    print_section("3. Counters with Attributes")
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=1, attributes=MetricAttributes.ENDPOINT_USERS.value)
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=1, attributes=MetricAttributes.ENDPOINT_ORDERS.value)
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=1, attributes=MetricAttributes.ENDPOINT_PRODUCTS.value)
    print_info("-> Same metric name, different attributes enable filtering/aggregation")
    
    # Example 4: Multiple counter types
    print_section("4. Different Counter Types")
    sdk.increment_counter(CounterName.CACHE_HITS.value, by=10, attributes=MetricAttributes.CACHE_HIT.value)
    sdk.increment_counter(CounterName.CACHE_MISSES.value, by=3, attributes=MetricAttributes.CACHE_MISS.value)
    sdk.increment_counter(CounterName.USER_LOGINS.value, by=5)
    sdk.increment_counter(CounterName.USER_SIGNUPS.value, by=2)
    sdk.increment_counter(CounterName.ERRORS.value, by=1, attributes=MetricAttributes.STATUS_ERROR.value)
    
    # Example 5: Regional tracking
    print_section("5. Multi-Dimensional Tracking")
    sdk.increment_counter(CounterName.REQUESTS_RECEIVED.value, by=100, attributes=MetricAttributes.REGION_US_EAST.value)
    sdk.increment_counter(CounterName.REQUESTS_RECEIVED.value, by=75, attributes=MetricAttributes.REGION_US_WEST.value)
    sdk.increment_counter(CounterName.REQUESTS_RECEIVED.value, by=50, attributes=MetricAttributes.REGION_EU_WEST.value)
    sdk.increment_counter(CounterName.REQUESTS_COMPLETED.value, by=225)
    print_info("-> Same metric with different region attributes tracked separately")
    
    # Example 6: Business metrics
    print_section("6. Business Metrics")
    sdk.increment_counter(CounterName.ORDERS_CREATED.value, by=10)
    sdk.increment_counter(CounterName.PAYMENTS_PROCESSED.value, by=10)
    
    # Example 7: Network traffic
    print_section("7. Network Traffic")
    sdk.increment_counter(CounterName.BYTES_SENT.value, by=1048576)
    sdk.increment_counter(CounterName.BYTES_RECEIVED.value, by=524288)
    print_info("-> Counters work well for tracking large numeric values")
    
    # Example 8: Floating-point counters (revenue tracking)
    print_section("8. Floating-Point Counters")
    sdk.increment_counter(CounterName.REVENUE_USD.value, by=MetricValues.REVENUE_SMALL.value)
    sdk.increment_counter(CounterName.REVENUE_USD.value, by=MetricValues.REVENUE_MEDIUM.value)
    sdk.increment_counter(CounterName.REVENUE_USD.value, by=MetricValues.REVENUE_LARGE.value)
    print_info("-> Counters support floating-point values (stored as asDouble)")
    
    print_footer("[OK] Example 14 completed successfully!")


if __name__ == "__main__":
    main()
