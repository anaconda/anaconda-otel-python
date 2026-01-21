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
    
    # Example 1: Active connections tracking
    print_section("2. Active Connections Tracking")
    sdk.increment_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=5)
    sdk.increment_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=3)
    sdk.decrement_counter(UpDownCounterName.ACTIVE_CONNECTIONS.value, by=2)
    print_info("→ Up/down counters can both increment and decrement")
    
    # Example 2: Queue size management
    print_section("3. Queue Size Management")
    sdk.increment_counter(UpDownCounterName.QUEUE_SIZE.value, by=10)
    sdk.decrement_counter(UpDownCounterName.QUEUE_SIZE.value, by=3)
    sdk.increment_counter(UpDownCounterName.QUEUE_SIZE.value, by=5)
    sdk.decrement_counter(UpDownCounterName.QUEUE_SIZE.value, by=8)
    
    # Example 3: Active users tracking
    print_section("4. Active Users Tracking")
    sdk.increment_counter(UpDownCounterName.ACTIVE_USERS.value, by=5)
    sdk.increment_counter(UpDownCounterName.ACTIVE_USERS.value, by=3)
    sdk.decrement_counter(UpDownCounterName.ACTIVE_USERS.value, by=2)
    
    # Example 4: Memory usage tracking
    print_section("5. Memory Usage Tracking")
    sdk.increment_counter(UpDownCounterName.MEMORY_USAGE_MB.value, by=256)
    sdk.increment_counter(UpDownCounterName.MEMORY_USAGE_MB.value, by=128)
    sdk.decrement_counter(UpDownCounterName.MEMORY_USAGE_MB.value, by=100)
    
    # Example 5: Concurrent requests with attributes
    print_section("6. Concurrent Requests by Region")
    sdk.increment_counter(UpDownCounterName.CONCURRENT_REQUESTS.value, by=10, attributes=MetricAttributes.REGION_US_EAST.value)
    sdk.increment_counter(UpDownCounterName.CONCURRENT_REQUESTS.value, by=7, attributes=MetricAttributes.REGION_US_WEST.value)
    sdk.decrement_counter(UpDownCounterName.CONCURRENT_REQUESTS.value, by=3, attributes=MetricAttributes.REGION_US_EAST.value)
    print_info("→ Track current state separately per region using attributes")
    
    # Example 6: Shopping cart items
    print_section("7. Shopping Cart Items")
    sdk.increment_counter(UpDownCounterName.ITEMS_IN_CART.value, by=3)
    sdk.increment_counter(UpDownCounterName.ITEMS_IN_CART.value, by=2)
    sdk.decrement_counter(UpDownCounterName.ITEMS_IN_CART.value, by=1)
    
    # Example 7: Additional up/down counters
    print_section("8. Additional Resource Tracking")
    sdk.increment_counter(UpDownCounterName.DISK_USAGE_GB.value, by=50)
    sdk.decrement_counter(UpDownCounterName.DISK_USAGE_GB.value, by=5)
    
    sdk.increment_counter(UpDownCounterName.ACTIVE_SESSIONS.value, by=5)
    sdk.increment_counter(UpDownCounterName.ACTIVE_SESSIONS.value, by=3)
    sdk.decrement_counter(UpDownCounterName.ACTIVE_SESSIONS.value, by=2)
    
    print_footer("✓ Example 16 completed successfully!")


if __name__ == "__main__":
    main()
