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
    print_section("1. Initialize Telemetry with Metrics")
    sdk.initialize(config, attrs, signal_types=['metrics'])
    
    # Send various metric types
    print_section("2. Send Different Metric Types")
    print_info("Counter metrics:")
    sdk.increment_counter(CounterName.API_REQUESTS.value, by=10, attributes=MetricAttributes.ENDPOINT_USERS.value)
    print_info(f"→ {MetricDescriptions.COUNTER.value}")
    
    sdk.increment_counter(CounterName.CACHE_HITS.value, by=50)
    
    print_info("Histogram metrics:")
    sdk.record_histogram(HistogramName.REQUEST_DURATION_MS.value, 15.5, attributes=MetricAttributes.HTTP_GET.value)
    print_info(f"→ {MetricDescriptions.HISTOGRAM.value}")
    
    sdk.record_histogram(HistogramName.DATABASE_QUERY_DURATION_MS.value, 125.0, attributes=MetricAttributes.DB_SELECT.value)
    
    print_info("Up/down counter metrics:")
    sdk.increment_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=5)
    print_info(f"→ {MetricDescriptions.UPDOWN_COUNTER.value}")
    
    sdk.decrement_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=2)
    
    print_info("✓ All metrics sent")
    
    # Explicit flush
    print_section("3. Explicit Flush")
    print_info("Flushing metrics telemetry data...")
    sdk.flush_metrics()
    print_info("✓ Flush completed successfully")
    print_info("\nNote: Python SDK automatically flushes on process exit.")
    print_info("Explicit flush is useful for:")
    print_info("  • Short-lived processes (Lambda, CLI tools)")
    print_info("  • Testing and validation")
    print_info("  • Ensuring metrics are sent before continuing")
    print_info("  • Batch jobs that need guaranteed delivery")
        
    print_footer("✓ Example 19 completed successfully!")


if __name__ == "__main__":
    main()
