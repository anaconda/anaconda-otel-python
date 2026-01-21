#!/usr/bin/env python3
"""
Example 18: Metrics Patterns and Best Practices

Demonstrates common metrics patterns and best practices for real-world scenarios.
Shows how to combine different metric types for comprehensive monitoring.

PATTERNS DEMONSTRATED:
- Request/Response pattern (latency + count + errors)
- RED metrics (Rate, Errors, Duration)
- Resource utilization pattern
- Business metrics pattern
- SLI/SLO tracking pattern

USE CASES:
- Production monitoring dashboards
- SLA/SLO tracking
- Performance monitoring
- Business KPI tracking
- Capacity planning

KEY CONCEPTS:
- Combine metric types for complete picture
- Use consistent naming across related metrics
- Track both technical and business metrics
- Enable SLO calculations
- Support alerting and dashboards
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
    ServiceNameMetrics
)

# Test data constants
SERVICE_NAME = ServiceNameMetrics.METRICS_PATTERNS.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value


def track_request(sdk: SdkOperations, endpoint: str, method: str, duration_ms: float, status_code: int):
    """
    Track a complete HTTP request with multiple metrics.
    This is the Request/Response pattern.
    """
    sdk.increment_counter("http_requests_total", by=1, attributes={"endpoint": endpoint, "method": method})
    sdk.record_histogram("http_request_duration_ms", duration_ms, attributes={"endpoint": endpoint, "method": method})
    sdk.increment_counter("http_responses_total", by=1, attributes={"endpoint": endpoint, "method": method, "status_code": status_code})
    
    if status_code >= 400:
        sdk.increment_counter("http_requests_errors_total", by=1, attributes={"endpoint": endpoint, "method": method, "status_code": status_code})


def track_database_operation(sdk: SdkOperations, operation: str, table: str, duration_ms: float, success: bool):
    """Track database operations with multiple metrics."""
    sdk.increment_counter("db_operations_total", by=1, attributes={"operation": operation, "table": table})
    sdk.record_histogram("db_operation_duration_ms", duration_ms, attributes={"operation": operation, "table": table})
    
    if not success:
        sdk.increment_counter("db_operations_errors_total", by=1, attributes={"operation": operation, "table": table})


def track_business_transaction(sdk: SdkOperations, transaction_type: str, amount_usd: float, success: bool):
    """Track business transactions with multiple metrics."""
    sdk.increment_counter("transactions_total", by=1, attributes={"type": transaction_type, "status": "success" if success else "failed"})
    
    if success:
        sdk.record_histogram("transaction_amount_usd", amount_usd, attributes={"type": transaction_type})
        # Store revenue in cents, using round() to avoid floating point precision issues
        sdk.increment_counter("revenue_total_usd", by=round(amount_usd * 100), attributes={"type": transaction_type})


def main():
    print_header("Example 18: Metrics Patterns and Best Practices", 
                 "Real-world metrics patterns for production monitoring")
    
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
    
    # Pattern 1: RED Metrics (Rate, Errors, Duration)
    print_section("2. Pattern: RED Metrics")
    print_info("RED metrics for comprehensive service monitoring:")
    print_info("  • Rate: Requests per second")
    print_info("  • Errors: Error rate")
    print_info("  • Duration: Response time distribution")
    
    print_info("Tracking successful requests:")
    for _ in range(10):
        track_request(sdk, "/api/users", "GET", 45.0, 200)
    print_info("→ 10 successful requests, avg 45ms")
    
    print_info("Tracking some errors:")
    for _ in range(2):
        track_request(sdk, "/api/users", "GET", 125.0, 500)
    print_info("→ 2 error requests")
    
    print_info("RED metrics calculated:")
    print_info("  • Rate: 12 requests")
    print_info("  • Errors: 2 errors (16.7% error rate)")
    print_info("  • Duration: p50, p95, p99 from histogram")
    
    # Pattern 2: Database monitoring
    print_section("3. Pattern: Database Monitoring")
    print_info("Track database operations comprehensively:")
    track_database_operation(sdk, "SELECT", "users", 15.0, True)
    track_database_operation(sdk, "SELECT", "users", 18.0, True)
    track_database_operation(sdk, "INSERT", "orders", 45.0, True)
    print_info("→ Successful operations tracked")
    
    track_database_operation(sdk, "UPDATE", "products", 3000.0, False)
    print_info("→ Failed operation tracked (timeout)")
    
    print_info("Database insights:")
    print_info("  • Operation count by type")
    print_info("  • Performance by table")
    print_info("  • Error rate by operation")
    print_info("  • Slow query detection (p95 > threshold)")
    
    # Pattern 3: Business metrics
    print_section("4. Pattern: Business Metrics")
    print_info("Track business KPIs alongside technical metrics:")
    track_business_transaction(sdk, "purchase", 49.99, True)
    track_business_transaction(sdk, "purchase", 99.99, True)
    track_business_transaction(sdk, "subscription", 19.99, True)
    print_info("→ Successful transactions: $169.97 revenue")
    
    track_business_transaction(sdk, "purchase", 199.99, False)
    print_info("→ Failed transaction tracked")
    
    print_info("Business insights:")
    print_info("  • Total revenue: $169.97")
    print_info("  • Transaction count: 4 (3 success, 1 failed)")
    print_info("  • Success rate: 75%")
    print_info("  • Average transaction value: $56.66")
    
    # Pattern 4: Resource utilization
    print_section("5. Pattern: Resource Utilization")
    print_info("Track resource usage over time:")
    sdk.increment_counter("active_connections", by=10)
    sdk.increment_counter("memory_usage_mb", by=512)
    sdk.record_histogram_batch("cpu_usage_percent", [45.5, 52.0, 48.5])
    
    print_info("Resource monitoring:")
    print_info("  • Active connections: 10")
    print_info("  • Memory usage: 512 MB")
    print_info("  • CPU usage: ~48.7% average")
    
    # Pattern 5: SLI/SLO tracking
    print_section("6. Pattern: SLI/SLO Tracking")
    print_info("Track metrics for SLO calculations:")
    print_info("Example SLO: 99% of requests complete in < 100ms")
    
    # Fast requests (meet SLO)
    sdk.record_histogram_batch("slo_request_duration_ms", [15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0], attributes={"slo_target": "100ms"})
    print_info("→ 9 requests under 100ms (meet SLO)")
    
    # Slow request (violates SLO)
    sdk.record_histogram("slo_request_duration_ms", 250.0, attributes={"slo_target": "100ms"})
    print_info("→ 1 request over 100ms (violates SLO)")
    
    print_info("SLO calculation:")
    print_info("  • Total requests: 10")
    print_info("  • Requests meeting SLO: 9")
    print_info("  • SLO compliance: 90% (below 99% target)")
    print_info("  • Action: Investigate slow request")
    
    # Best practices summary
    print_section("7. Metrics Best Practices Summary")
    print_info("Naming conventions:")
    print_info("  • Use consistent suffixes: _total, _duration_ms, _bytes")
    print_info("  • Group related metrics: http_*, db_*, business_*")
    print_info("  • Be descriptive: http_request_duration_ms not latency")
    print_info("\nMetric selection:")
    print_info("  • Counters: Totals, rates, cumulative values")
    print_info("  • Histograms: Durations, sizes, distributions")
    print_info("  • Up/Down Counters: Current state, resource usage")
    print_info("\nCombining metrics:")
    print_info("  • Track rate + errors + duration (RED)")
    print_info("  • Combine technical + business metrics")
    print_info("  • Enable SLO calculations")
    print_info("  • Support multiple analysis dimensions")
    print_info("\nProduction patterns:")
    print_info("  • Always track errors separately")
    print_info("  • Use histograms for latency")
    print_info("  • Track both count and duration")
    print_info("  • Include attributes for filtering")
    print_info("  • Monitor resource utilization")
        
    print_footer("✓ Example 18 completed successfully!")


if __name__ == "__main__":
    main()
