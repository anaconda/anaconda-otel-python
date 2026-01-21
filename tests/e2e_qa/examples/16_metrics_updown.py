#!/usr/bin/env python3
"""
Example 16: Up/Down Counter Metrics

Demonstrates using up/down counters to track values that can increase or decrease.
Unlike regular counters, up/down counters can go both up and down.

WHEN TO USE UP/DOWN COUNTERS:
- Track current state that changes (active connections, queue size)
- Monitor resource usage (memory, disk space)
- Count items that can be added or removed (cart items, active users)
- Track concurrent operations (active requests, running tasks)

USE CASES:
- Active connection tracking
- Queue size monitoring
- Memory/disk usage tracking
- Active user sessions
- Concurrent request counting
- Items in shopping cart
- Active background tasks

KEY CONCEPTS:
- Up/down counters can increase AND decrease
- Use increment_counter() to increase
- Use decrement_counter() to decrease
- Tracks current state, not just totals
- Useful for gauges and current values
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
    UpDownCounterName,
    MetricAttributes,
    MetricValues,
    MetricDescriptions
)

# Test data constants
SERVICE_NAME = ServiceNameMetrics.METRICS_UPDOWN.value
SERVICE_VERSION = ServiceVersion.DEFAULT.value


def main():
    print_header("Example 16: Up/Down Counter Metrics", 
                 "Track values that can increase or decrease")
    
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
    
    # Example 1: Active connections tracking
    print_section("2. Active Connections Tracking")
    print_info("Simulating connection lifecycle:")
    sdk.increment_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=5)
    print_info("→ Active connections: 5")
    
    sdk.increment_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=3)
    print_info("→ Active connections: 8 (5 + 3)")
    
    sdk.decrement_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=2)
    print_info("→ Active connections: 6 (8 - 2)")
    
    # Example 2: Queue size management
    print_section("3. Queue Size Management")
    print_info("Simulating message queue operations:")
    sdk.increment_counter(UpDownCounterName.QUEUE_SIZE.value, by=10)
    print_info("→ Queue size: 10")
    
    sdk.decrement_counter(UpDownCounterName.QUEUE_SIZE.value, by=3)
    print_info("→ Queue size: 7 (10 - 3)")
    
    sdk.increment_counter(UpDownCounterName.QUEUE_SIZE.value, by=5)
    print_info("→ Queue size: 12 (7 + 5)")
    
    sdk.decrement_counter(UpDownCounterName.QUEUE_SIZE.value, by=8)
    print_info("→ Queue size: 4 (12 - 8)")
    
    # Example 3: Active users tracking
    print_section("4. Active Users Tracking")
    print_info("Track users logging in and out:")
    sdk.increment_counter(UpDownCounterName.ACTIVE_USERS.value, by=5)
    sdk.increment_counter(UpDownCounterName.ACTIVE_USERS.value, by=3)
    print_info("→ Active users: 8")
    
    sdk.decrement_counter(UpDownCounterName.ACTIVE_USERS.value, by=2)
    print_info("→ Active users: 6")
    
    # Example 4: Memory usage tracking
    print_section("5. Memory Usage Tracking")
    print_info("Track memory allocation and deallocation:")
    sdk.increment_counter(UpDownCounterName.MEMORY_USAGE_MB.value, by=256)
    sdk.increment_counter(UpDownCounterName.MEMORY_USAGE_MB.value, by=128)
    print_info("→ Memory usage: 384 MB")
    
    sdk.decrement_counter(UpDownCounterName.MEMORY_USAGE_MB.value, by=100)
    print_info("→ Memory usage: 284 MB")
    
    # Example 5: Concurrent requests with attributes
    print_section("6. Concurrent Requests by Region")
    print_info("Track concurrent requests across regions:")
    sdk.increment_counter(UpDownCounterName.CONCURRENT_REQUESTS.value, by=10, attributes=MetricAttributes.REGION_US_EAST.value)
    print_info("→ US East: 10 concurrent requests")
    
    sdk.increment_counter(UpDownCounterName.CONCURRENT_REQUESTS.value, by=7, attributes=MetricAttributes.REGION_US_WEST.value)
    print_info("→ US West: 7 concurrent requests")
    
    sdk.decrement_counter(UpDownCounterName.CONCURRENT_REQUESTS.value, by=3, attributes=MetricAttributes.REGION_US_EAST.value)
    print_info("→ US East: 7 concurrent requests (10 - 3)")
    
    # Example 6: Shopping cart items
    print_section("7. Shopping Cart Items")
    print_info("Track items added/removed from cart:")
    sdk.increment_counter(UpDownCounterName.ITEMS_IN_CART.value, by=3)
    sdk.increment_counter(UpDownCounterName.ITEMS_IN_CART.value, by=2)
    print_info("→ Cart items: 5")
    
    sdk.decrement_counter(UpDownCounterName.ITEMS_IN_CART.value, by=1)
    print_info("→ Cart items: 4")
    
    # Example 7: Additional up/down counters
    print_section("8. Additional Resource Tracking")
    print_info("Disk usage tracking:")
    sdk.increment_counter(UpDownCounterName.DISK_USAGE_GB.value, by=50)
    sdk.decrement_counter(UpDownCounterName.DISK_USAGE_GB.value, by=5)
    print_info("→ Disk usage: 45 GB (50 - 5)")
    
    print_info("Active sessions tracking:")
    sdk.increment_counter(UpDownCounterName.ACTIVE_SESSIONS.value, by=5)
    sdk.increment_counter(UpDownCounterName.ACTIVE_SESSIONS.value, by=3)
    sdk.decrement_counter(UpDownCounterName.ACTIVE_SESSIONS.value, by=2)
    print_info("→ Active sessions: 6 (5 + 3 - 2)")
    
    # Best practices
    print_section("9. Up/Down Counter Best Practices")
    print_info(f"What is an up/down counter? {MetricDescriptions.UPDOWN_COUNTER.value}")
    print_info("When to use up/down counters:")
    print_info("  ✓ Current state that changes (active connections)")
    print_info("  ✓ Resource usage (memory, disk)")
    print_info("  ✓ Queue sizes and backlogs")
    print_info("  ✓ Active sessions or users")
    print_info("  ✓ Concurrent operations")
    print_info("  ✗ Totals that only increase (use regular counter)")
    print_info("  ✗ Distributions of values (use histogram)")
    print_info("\nNaming conventions:")
    print_info("  • Describe current state: 'active_connections' not 'connections_total'")
    print_info("  • Omit '_total' suffix (not a cumulative total)")
    print_info("  • Use descriptive names: 'queue_size', 'memory_usage_mb'")
    print_info("\nCommon patterns:")
    print_info("  • Increment when resource acquired/added")
    print_info("  • Decrement when resource released/removed")
    print_info("  • Track current state, not historical totals")
    print_info("  • Use attributes for multi-dimensional tracking")
        
    print_footer("✓ Example 16 completed successfully!")


if __name__ == "__main__":
    main()
