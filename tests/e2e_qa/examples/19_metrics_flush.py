#!/usr/bin/env python3
"""
Example 19: Metrics with Explicit Flush

Demonstrates explicit flush functionality for metrics to ensure telemetry data
is sent before the application exits. Similar to Example 7 but focused on metrics.

WHEN TO USE THIS APPROACH:
- Short-lived processes or scripts that need guaranteed metric delivery
- Lambda functions or serverless applications
- Testing and validation scenarios where you need to confirm metrics were sent
- Applications that need to ensure metrics are exported before shutdown
- Batch jobs or CLI tools with critical metrics

USE CASES:
- Short-lived CLI tools or batch jobs
- Lambda functions or serverless applications
- Testing and validation scenarios
- Applications where you need guaranteed delivery before shutdown
- Scripts that need to confirm metric export completed

NOTE: For Python, the OpenTelemetry SDK automatically handles flushing when
the process ends. Explicit flush is typically not necessary but is supported
for cases where you need immediate export or want to ensure data is sent
before continuing execution.
"""

from anaconda.opentelemetry import (
    Configuration, 
    ResourceAttributes, 
    initialize_telemetry,
    increment_counter,
    record_histogram,
    decrement_counter
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
    flush_metrics,
    apply_signal_specific_endpoints
)
from test_data import (
    ServiceVersion,
    ServiceNameMetrics,
    CounterName,
    HistogramName,
    UpDownCounterName,
    MetricAttributes,
    MetricValues,
    MetricDescriptions
)

# Test data constants
SERVICE_NAME = ServiceNameMetrics.METRICS_FLUSH.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value


def main():
    print_header("Example 19: Metrics with Explicit Flush", 
                 "Verify flush functionality for metrics doesn't break telemetry flow")
    
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
    print_section("1. Initialize Telemetry with Metrics")
    initialize_telemetry(
        config=config,
        attributes=attrs,
        signal_types=['metrics']
    )
    print_code("initialize_telemetry(config, attrs, signal_types=['metrics'])")
    print_info("✓ Telemetry initialized with metrics enabled")
    
    # Send various metric types
    print_section("2. Send Different Metric Types")
    
    print_info("\n  Counter metrics:")
    increment_counter(CounterName.API_REQUESTS.value, by=MetricValues.INCREMENT_TEN.value, attributes=MetricAttributes.ENDPOINT_USERS.value)
    print_code(f'increment_counter("{CounterName.API_REQUESTS.value}", by=10, attributes=ENDPOINT_USERS)')
    print_info(f"    → {MetricDescriptions.COUNTER.value}")
    
    increment_counter(CounterName.CACHE_HITS.value, by=50)
    print_code(f'increment_counter("{CounterName.CACHE_HITS.value}", by=50)')
    
    print_info("\n  Histogram metrics:")
    record_histogram(HistogramName.REQUEST_DURATION_MS.value, MetricValues.FAST_RESPONSE.value, attributes=MetricAttributes.HTTP_GET.value)
    print_code(f'record_histogram("{HistogramName.REQUEST_DURATION_MS.value}", 15.5, attributes=HTTP_GET)')
    print_info(f"    → {MetricDescriptions.HISTOGRAM.value}")
    
    record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, MetricValues.NORMAL_RESPONSE.value, attributes=MetricAttributes.DB_SELECT.value)
    print_code(f'record_histogram("{HistogramName.DATABASE_QUERY_DURATION_MS.value}", 125.0, attributes=DB_SELECT)')
    
    print_info("\n  Up/down counter metrics:")
    increment_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=MetricValues.INCREASE_FIVE.value)
    print_code(f'increment_counter("{UpDownCounterName.ACTIVE_CONNECTIONS.value}", by=5)')
    print_info(f"    → {MetricDescriptions.UPDOWN_COUNTER.value}")
    
    decrement_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=2)
    print_code(f'decrement_counter("{UpDownCounterName.ACTIVE_CONNECTIONS.value}", by=2)')
    
    print_info("\n✓ All metrics sent")
    
    # Explicit flush
    print_section("3. Explicit Flush")
    print_info("Flushing metrics telemetry data...")
    print_code("flush_metrics()")
    flush_metrics()
    print_info("✓ Flush completed successfully")
    print_info("\nNote: Python SDK automatically flushes on process exit.")
    print_info("Explicit flush is useful for:")
    print_info("  • Short-lived processes (Lambda, CLI tools)")
    print_info("  • Testing and validation")
    print_info("  • Ensuring metrics are sent before continuing")
    print_info("  • Batch jobs that need guaranteed delivery")
    
    # SDK Commands Summary
    print_section("SDK Commands Summary")
    print_info("Commands used in this example:")
    print_code("1. initialize_telemetry(config, attrs, signal_types=['metrics'])")
    print_code("2. increment_counter(name, by=value, attributes={...})")
    print_code("3. record_histogram(name, value, attributes={...})")
    print_code("4. decrement_counter(name, by=value)")
    print_code("5. flush_metrics()  # Explicitly flush metrics data")
    
    # Backend validation
    print_section("Backend Validation")
    print_info("To validate in backend:")
    print_info(f"  • Service Name: {SERVICE_NAME}")
    print_info(f"  • Service Version: {SERVICE_VERSION}")
    print_info("  • Expected metrics:")
    print_info(f"    - {CounterName.API_REQUESTS.value}: 10 (with endpoint attributes)")
    print_info(f"    - {CounterName.CACHE_HITS.value}: 50")
    print_info(f"    - {HistogramName.REQUEST_DURATION_MS.value}: 1 measurement (15.5ms)")
    print_info(f"    - {HistogramName.DATABASE_QUERY_DURATION_MS.value}: 1 measurement (125.0ms)")
    print_info(f"    - {UpDownCounterName.ACTIVE_CONNECTIONS.value}: 3 (5 - 2)")
    print_info("  • All metrics should have resource attributes")
    print_info("  • Metrics should appear in backend within export interval")
    
    print_footer("✓ Example 19 completed successfully!")


if __name__ == "__main__":
    main()
