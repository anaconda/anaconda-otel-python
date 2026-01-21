#!/usr/bin/env python3
"""
Example 15: Histogram Metrics

Demonstrates using histogram metrics to track distributions of values.
Histograms are ideal for measuring latencies, sizes, and other continuous values.

WHEN TO USE HISTOGRAMS:
- Measure request/response durations
- Track data sizes (request/response bytes, file sizes)
- Record business metrics (order values, transaction amounts)
- Monitor performance metrics (query times, processing times)
- Analyze value distributions (percentiles, averages)

USE CASES:
- API response time tracking
- Database query duration monitoring
- File size distribution
- Order value analysis
- Memory usage patterns
- Network latency measurements

KEY CONCEPTS:
- Histograms record distributions of values
- Use record_histogram() to record a value
- Backend calculates percentiles (p50, p95, p99)
- Histograms track count, sum, min, max automatically
- Attributes enable multi-dimensional analysis
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
    HistogramName,
    MetricAttributes,
    MetricValues,
    MetricDescriptions
)

# Test data constants
SERVICE_NAME = ServiceNameMetrics.METRICS_HISTOGRAM.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value


def main():
    print_header("Example 15: Histogram Metrics", 
                 "Track distributions of values with histograms")
    
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
    
    # Example 1: Basic histogram recording
    print_section("2. Basic Histogram Usage")
    sdk.record_histogram(HistogramName.REQUEST_DURATION_MS.value, 125.5)
    
    # Example 2: Multiple values for distribution
    print_section("3. Recording Multiple Values")
    durations = [15.5, 23.0, 125.0, 45.0, 850.0, 32.0, 67.0]
    sdk.record_histogram_batch(HistogramName.REQUEST_DURATION_MS.value, durations)
    print_info("→ Backend calculates min, max, avg, p50, p95, p99 from distribution")
    
    # Example 3: Histogram with attributes
    print_section("4. Histograms with Attributes")
    sdk.record_histogram(HistogramName.API_RESPONSE_TIME_MS.value, 45.5, attributes=MetricAttributes.ENDPOINT_USERS.value)
    sdk.record_histogram(HistogramName.API_RESPONSE_TIME_MS.value, 125.0, attributes=MetricAttributes.ENDPOINT_ORDERS.value)
    sdk.record_histogram(HistogramName.API_RESPONSE_TIME_MS.value, 32.0, attributes=MetricAttributes.ENDPOINT_PRODUCTS.value)
    print_info("→ Attributes enable performance comparison across dimensions")
    
    # Example 4: Database query durations
    print_section("5. Database Query Duration Tracking")
    sdk.record_histogram_batch(HistogramName.DATABASE_QUERY_DURATION_MS.value, [15.5] * 5, attributes=MetricAttributes.DB_SELECT.value)
    sdk.record_histogram_batch(HistogramName.DATABASE_QUERY_DURATION_MS.value, [45.0] * 3, attributes=MetricAttributes.DB_INSERT.value)
    sdk.record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, 125.0, attributes=MetricAttributes.DB_UPDATE.value)
    
    # Example 5: Data size tracking
    print_section("6. Data Size Tracking")
    request_sizes = [1024, 2048, 512, 10240, 5120]
    sdk.record_histogram_batch(HistogramName.REQUEST_SIZE_BYTES.value, request_sizes)
    
    response_sizes = [512, 1024, 102400, 2048, 50000]
    sdk.record_histogram_batch(HistogramName.RESPONSE_SIZE_BYTES.value, response_sizes)
    
    # Example 6: Business metrics
    print_section("7. Business Metrics Tracking")
    order_values = [9.99, 49.99, 19.99, 199.99, 29.99, 99.99, 14.99]
    sdk.record_histogram_batch(HistogramName.ORDER_VALUE_USD.value, order_values, attributes=MetricAttributes.STATUS_SUCCESS.value)
    print_info("→ Histograms enable business analysis: total revenue, average order value, percentiles")
    
    # Example 7: Additional histogram types
    print_section("8. Additional Histogram Types")
    sdk.record_histogram(HistogramName.CACHE_LOOKUP_DURATION_MS.value, 15.5)
    sdk.record_histogram_batch(HistogramName.FILE_SIZE_BYTES.value, [1024, 10240, 102400])
    sdk.record_histogram(HistogramName.CART_VALUE_USD.value, 75.50)
    sdk.record_histogram(HistogramName.TRANSACTION_AMOUNT_USD.value, 250.00)
    
    print_footer("✓ Example 15 completed successfully!")


if __name__ == "__main__":
    main()
