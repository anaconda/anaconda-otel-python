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

from anaconda.opentelemetry import (
    Configuration, 
    ResourceAttributes, 
    initialize_telemetry,
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
    
    # Example 1: Basic histogram recording
    print_section("2. Basic Histogram Usage")
    print_info("\n  Example 1: Record a single value")
    record_histogram(HistogramName.REQUEST_DURATION_MS.value, 125.5)
    print_code(f'record_histogram("{HistogramName.REQUEST_DURATION_MS.value}", 125.5)')
    print_info("    → Records request duration of 125.5 milliseconds")
    
    # Example 2: Multiple values for distribution
    print_info("\n  Example 2: Record multiple values to see distribution")
    durations = [
        MetricValues.FAST_RESPONSE.value,
        23.0,
        MetricValues.NORMAL_RESPONSE.value,
        45.0,
        MetricValues.SLOW_RESPONSE.value,
        32.0,
        67.0
    ]
    for duration in durations:
        record_histogram(HistogramName.REQUEST_DURATION_MS.value, duration)
    print_code(f'for duration in [15.5, 23.0, 125.0, 45.0, 850.0, 32.0, 67.0]:')
    print_code(f'    record_histogram("{HistogramName.REQUEST_DURATION_MS.value}", duration)')
    print_info(f"    → Recorded {len(durations)} values")
    print_info("    → Backend calculates: min, max, avg, p50, p95, p99")
    
    # Example 3: Histogram with attributes
    print_section("3. Histograms with Attributes")
    print_info("\n  Example 3: Track API response times by endpoint")
    
    # Track different endpoints
    record_histogram(
        HistogramName.API_RESPONSE_TIME_MS.value,
        45.5,
        attributes=MetricAttributes.ENDPOINT_USERS.value
    )
    print_code(f'record_histogram("{HistogramName.API_RESPONSE_TIME_MS.value}", 45.5, attributes={MetricAttributes.ENDPOINT_USERS.value})')
    
    record_histogram(
        HistogramName.API_RESPONSE_TIME_MS.value,
        125.0,
        attributes=MetricAttributes.ENDPOINT_ORDERS.value
    )
    print_code(f'record_histogram("{HistogramName.API_RESPONSE_TIME_MS.value}", 125.0, attributes={MetricAttributes.ENDPOINT_ORDERS.value})')
    
    record_histogram(
        HistogramName.API_RESPONSE_TIME_MS.value,
        32.0,
        attributes=MetricAttributes.ENDPOINT_PRODUCTS.value
    )
    print_code(f'record_histogram("{HistogramName.API_RESPONSE_TIME_MS.value}", 32.0, attributes={MetricAttributes.ENDPOINT_PRODUCTS.value})')
    
    print_info("    → Same metric name, different endpoints")
    print_info("    → Can compare performance across endpoints")
    
    # Example 4: Database query durations
    print_section("4. Database Query Duration Tracking")
    print_info("\n  Track query performance by operation type:")
    
    # SELECT queries (typically fast)
    for _ in range(5):
        record_histogram(
            HistogramName.DATABASE_QUERY_DURATION_MS.value,
            15.5,
            attributes=MetricAttributes.DB_SELECT.value
        )
    print_code(f'record_histogram("{HistogramName.DATABASE_QUERY_DURATION_MS.value}", 15.5, attributes=DB_SELECT)')
    print_info("    → Recorded 5 fast SELECT queries")
    
    # INSERT queries (typically slower)
    for _ in range(3):
        record_histogram(
            HistogramName.DATABASE_QUERY_DURATION_MS.value,
            45.0,
            attributes=MetricAttributes.DB_INSERT.value
        )
    print_code(f'record_histogram("{HistogramName.DATABASE_QUERY_DURATION_MS.value}", 45.0, attributes=DB_INSERT)')
    print_info("    → Recorded 3 slower INSERT queries")
    
    # UPDATE queries (variable)
    record_histogram(
        HistogramName.DATABASE_QUERY_DURATION_MS.value,
        125.0,
        attributes=MetricAttributes.DB_UPDATE.value
    )
    print_code(f'record_histogram("{HistogramName.DATABASE_QUERY_DURATION_MS.value}", 125.0, attributes=DB_UPDATE)')
    print_info("    → Recorded 1 UPDATE query")
    
    # Example 5: Data size tracking
    print_section("5. Data Size Tracking")
    print_info("\n  Track request and response sizes:")
    
    # Request sizes
    request_sizes = [1024, 2048, 512, 10240, 5120]
    for size in request_sizes:
        record_histogram(HistogramName.REQUEST_SIZE_BYTES.value, size)
    print_code(f'for size in {request_sizes}:')
    print_code(f'    record_histogram("{HistogramName.REQUEST_SIZE_BYTES.value}", size)')
    print_info(f"    → Recorded {len(request_sizes)} request sizes")
    
    # Response sizes
    response_sizes = [512, 1024, 102400, 2048, 50000]
    for size in response_sizes:
        record_histogram(HistogramName.RESPONSE_SIZE_BYTES.value, size)
    print_code(f'for size in {response_sizes}:')
    print_code(f'    record_histogram("{HistogramName.RESPONSE_SIZE_BYTES.value}", size)')
    print_info(f"    → Recorded {len(response_sizes)} response sizes")
    
    # Example 6: Business metrics
    print_section("6. Business Metrics Tracking")
    print_info("\n  Track order values for business analysis:")
    
    order_values = [
        MetricValues.SMALL_ORDER.value,
        MetricValues.MEDIUM_ORDER.value,
        19.99,
        MetricValues.LARGE_ORDER.value,
        29.99,
        99.99,
        14.99
    ]
    for value in order_values:
        record_histogram(
            HistogramName.ORDER_VALUE_USD.value,
            value,
            attributes=MetricAttributes.STATUS_SUCCESS.value
        )
    print_code(f'for value in [9.99, 49.99, 19.99, 199.99, 29.99, 99.99, 14.99]:')
    print_code(f'    record_histogram("{HistogramName.ORDER_VALUE_USD.value}", value, attributes=STATUS_SUCCESS)')
    print_info(f"    → Recorded {len(order_values)} order values")
    print_info("    → Backend can calculate: total revenue, average order value")
    print_info("    → Percentiles show: p50 (median), p95, p99 order values")
    
    # Example 7: Additional histogram types
    print_section("7. Additional Histogram Types")
    
    print_info("\n  Cache lookup duration:")
    record_histogram(HistogramName.CACHE_LOOKUP_DURATION_MS.value, MetricValues.FAST_RESPONSE.value)
    print_code(f'record_histogram("{HistogramName.CACHE_LOOKUP_DURATION_MS.value}", 15.5)')
    
    print_info("\n  File sizes:")
    for size in [MetricValues.SMALL_SIZE.value, MetricValues.MEDIUM_SIZE.value, MetricValues.LARGE_SIZE.value]:
        record_histogram(HistogramName.FILE_SIZE_BYTES.value, size)
    print_code(f'record_histogram("{HistogramName.FILE_SIZE_BYTES.value}", [1024, 10240, 102400])')
    
    print_info("\n  Shopping cart values:")
    record_histogram(HistogramName.CART_VALUE_USD.value, 75.50)
    print_code(f'record_histogram("{HistogramName.CART_VALUE_USD.value}", 75.50)')
    
    print_info("\n  Transaction amounts:")
    record_histogram(HistogramName.TRANSACTION_AMOUNT_USD.value, 250.00)
    print_code(f'record_histogram("{HistogramName.TRANSACTION_AMOUNT_USD.value}", 250.00)')
    
    # Best practices
    print_section("8. Histogram Best Practices")
    print_info(f"What is a histogram? {MetricDescriptions.HISTOGRAM.value}")
    print_info("Naming conventions:")
    print_info("  • Include units: '_ms' for milliseconds, '_bytes' for bytes")
    print_info("  • Use 'duration' for time: 'request_duration_ms'")
    print_info("  • Use 'size' for bytes: 'response_size_bytes'")
    print_info("  • Be descriptive: 'database_query_duration_ms'")
    print_info("\nWhen to use histograms:")
    print_info("  ✓ Measuring durations/latencies")
    print_info("  ✓ Tracking sizes (bytes, items, etc.)")
    print_info("  ✓ Recording continuous values")
    print_info("  ✓ Analyzing distributions and percentiles")
    print_info("  ✗ Simple counts (use counter)")
    print_info("  ✗ Current values that go up/down (use up/down counter)")
    print_info("\nAnalysis capabilities:")
    print_info("  • Percentiles: p50 (median), p95, p99")
    print_info("  • Statistics: min, max, average, sum, count")
    print_info("  • Distribution: See how values are spread")
    print_info("  • Outliers: Identify slow requests or large payloads")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. initialize_telemetry(config, attrs, signal_types=['metrics'])")
    print_code("2. record_histogram(name, value)")
    print_code("3. record_histogram(name, value, attributes={'key': 'value'})")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected histogram metrics:")
    print_info(f"    - {HistogramName.REQUEST_DURATION_MS.value}: 8 values (1 + 7)")
    print_info(f"    - {HistogramName.API_RESPONSE_TIME_MS.value}: 3 values (different endpoints)")
    print_info(f"    - {HistogramName.DATABASE_QUERY_DURATION_MS.value}: 9 values (5 + 3 + 1)")
    print_info(f"    - {HistogramName.REQUEST_SIZE_BYTES.value}: 5 values")
    print_info(f"    - {HistogramName.RESPONSE_SIZE_BYTES.value}: 5 values")
    print_info(f"    - {HistogramName.ORDER_VALUE_USD.value}: 7 values")
    print_info(f"    - {HistogramName.CACHE_LOOKUP_DURATION_MS.value}: 1 value")
    print_info(f"    - {HistogramName.FILE_SIZE_BYTES.value}: 3 values")
    print_info(f"    - {HistogramName.CART_VALUE_USD.value}: 1 value")
    print_info(f"    - {HistogramName.TRANSACTION_AMOUNT_USD.value}: 1 value")
    print_info("  • For each histogram, backend should show:")
    print_info("    - Count, sum, min, max")
    print_info("    - Percentiles (p50, p95, p99)")
    print_info("    - Distribution visualization")
    
    print_footer("✓ Example 15 completed successfully!")


if __name__ == "__main__":
    main()
