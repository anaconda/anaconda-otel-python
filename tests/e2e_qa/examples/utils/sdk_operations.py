# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
SDK Operations with Integrated Logging

This module provides wrapper functions for SDK operations that include
integrated detailed logging. This keeps example code clean and concise
while still providing comprehensive logging when USE_DETAILED_LOG=true.

Usage:
    from utils.sdk_operations import SdkOperations
    
    sdk = SdkOperations(endpoint="http://localhost:4318")
    
    # Initialize telemetry with logging
    sdk.initialize(config, attrs, signal_types=['metrics'])
    
    # Increment counter with logging
    sdk.increment_counter("api_requests_total", by=100, 
                         attributes={"http.method": "GET"})
    
    # Record histogram with logging
    sdk.record_histogram("request_duration_ms", 45.0,
                        attributes={"region": "us-east"})
"""

import time
from typing import Any, Dict, List, Optional, Union
from anaconda.opentelemetry import (
    Configuration,
    ResourceAttributes,
    initialize_telemetry,
    increment_counter,
    decrement_counter,
    record_histogram,
)
from .print_utils import log_detailed, print_code


class SdkOperations:
    """
    Wrapper class for SDK operations with integrated detailed logging.
    
    This class wraps all SDK operations and adds detailed logging when
    USE_DETAILED_LOG environment variable is enabled. This keeps example
    code clean while providing comprehensive debugging information.
    
    Attributes:
        endpoint: The telemetry endpoint URL
        service_name: Service name for logging context
        service_version: Service version for logging context
        show_code: Whether to print code examples (default: True)
    """
    
    def __init__(self, endpoint: str = "", service_name: str = "", service_version: str = "", show_code: bool = True):
        """
        Initialize SDK operations wrapper.
        
        Args:
            endpoint: Target endpoint URL (optional, for logging)
            service_name: Service name (optional, for logging)
            service_version: Service version (optional, for logging)
            show_code: Whether to print code examples (default: True)
        """
        self.endpoint = endpoint
        self.service_name = service_name
        self.service_version = service_version
        self.show_code = show_code
    
    def _format_attributes(self, attributes: Optional[Dict[str, Any]]) -> str:
        """Format attributes for display in code examples."""
        if not attributes:
            return ""
        # Format as a compact dict representation
        items = [f'"{k}": {repr(v)}' for k, v in attributes.items()]
        return "{" + ", ".join(items) + "}"
    
    def initialize(
        self,
        config: Configuration,
        attributes: ResourceAttributes,
        signal_types: Optional[List[str]] = None
    ) -> None:
        """
        Initialize telemetry with detailed logging.
        
        Args:
            config: Configuration object
            attributes: Resource attributes
            signal_types: List of signal types to enable
        """
        # Print the code being executed
        if self.show_code:
            signal_str = f"signal_types={signal_types}" if signal_types else ""
            print_code(f"initialize_telemetry(config, attrs{', ' + signal_str if signal_str else ''})")
        
        log_detailed("Calling initialize_telemetry()...")
        log_detailed(f"  Config: endpoint={self.endpoint}")
        log_detailed(f"  Attributes: service_name={self.service_name}, service_version={self.service_version}")
        log_detailed(f"  Signal types: {signal_types}")
        
        start_time = time.time()
        initialize_telemetry(
            config=config,
            attributes=attributes,
            signal_types=signal_types
        )
        duration = time.time() - start_time
        
        log_detailed(f"✓ Initialization completed in {duration:.3f}s")
        
        # Log which providers are ready
        if signal_types:
            for signal in signal_types:
                log_detailed(f"✓ {signal.capitalize()} provider ready to accept {signal}")
    
    def increment_counter(
        self,
        name: str,
        by: Union[int, float] = 1,
        attributes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> None:
        """
        Increment a counter with detailed logging.
        
        Args:
            name: Counter name
            by: Amount to increment by
            attributes: Optional attributes dictionary
            description: Optional description for logging
        """
        # Print the code being executed
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            by_str = f", by={by}" if by != 1 else ""
            print_code(f'increment_counter("{name}"{by_str}{attrs_str})')
        
        # Build log message
        log_msg = f"Sending counter: {name}"
        if description:
            log_msg += f" ({description})"
        log_detailed(log_msg)
        
        log_detailed(f"  → Metric: {name}")
        log_detailed(f"  → Value: {by}")
        if attributes:
            log_detailed(f"  → Attributes: {attributes}")
        if self.endpoint:
            log_detailed(f"  → Endpoint: {self.endpoint}")
        
        start_time = time.time()
        increment_counter(name, by=by, attributes=attributes or {})
        duration = time.time() - start_time
        
        log_detailed(f"✓ Counter queued successfully (took {duration:.3f}s)")
        log_detailed("✓ SDK accepted metric, will export in background")
    
    def record_histogram(
        self,
        name: str,
        value: Union[int, float],
        attributes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> None:
        """
        Record a histogram value with detailed logging.
        
        Args:
            name: Histogram name
            value: Value to record
            attributes: Optional attributes dictionary
            description: Optional description for logging
        """
        # Print the code being executed
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            print_code(f'record_histogram("{name}", {value}{attrs_str})')
        
        # Build log message
        log_msg = f"Sending histogram: {name}"
        if description:
            log_msg += f" ({description})"
        log_detailed(log_msg)
        
        log_detailed(f"  → Metric: {name}")
        log_detailed(f"  → Value: {value}")
        if attributes:
            log_detailed(f"  → Attributes: {attributes}")
        if self.endpoint:
            log_detailed(f"  → Endpoint: {self.endpoint}")
        
        start_time = time.time()
        record_histogram(name, value, attributes=attributes or {})
        duration = time.time() - start_time
        
        log_detailed(f"✓ Histogram queued successfully (took {duration:.3f}s)")
        log_detailed("✓ SDK accepted metric, will export in background")
    
    def record_histogram_batch(
        self,
        name: str,
        values: List[Union[int, float]],
        attributes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> None:
        """
        Record multiple histogram values with detailed logging.
        
        This is useful when recording multiple measurements for the same
        metric with the same attributes (e.g., multiple latency samples).
        
        Args:
            name: Histogram name
            values: List of values to record
            attributes: Optional attributes dictionary
            description: Optional description for logging
        """
        # Print the code being executed (show loop pattern)
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            print_code(f'record_histogram("{name}", value{attrs_str})  # {len(values)} times')
        
        # Build log message
        log_msg = f"Sending histograms: {name}"
        if description:
            log_msg += f" ({description})"
        log_detailed(log_msg)
        
        log_detailed(f"  → Metric: {name}")
        if attributes:
            log_detailed(f"  → Attributes: {attributes}")
        log_detailed(f"  → Values: {values}")
        
        start_time = time.time()
        for i, value in enumerate(values, 1):
            record_histogram(name, value, attributes=attributes or {})
            log_detailed(f"  → Histogram {i}/{len(values)}: {value} queued")
        total_duration = time.time() - start_time
        
        log_detailed(f"✓ All {len(values)} histograms queued successfully (took {total_duration:.3f}s)")
        log_detailed("✓ SDK accepted metrics, will export in background")
    
    def decrement_counter(
        self,
        name: str,
        by: Union[int, float] = 1,
        attributes: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> None:
        """
        Decrement a counter with detailed logging.
        
        Args:
            name: Counter name
            by: Amount to decrement by
            attributes: Optional attributes dictionary
            description: Optional description for logging
        """
        # Print the code being executed
        if self.show_code:
            attrs_str = f", attributes={self._format_attributes(attributes)}" if attributes else ""
            by_str = f", by={by}" if by != 1 else ""
            print_code(f'decrement_counter("{name}"{by_str}{attrs_str})')
        
        # Build log message
        log_msg = f"Sending decrement counter: {name}"
        if description:
            log_msg += f" ({description})"
        log_detailed(log_msg)
        
        log_detailed(f"  → Metric: {name}")
        log_detailed(f"  → Value: -{by}")
        if attributes:
            log_detailed(f"  → Attributes: {attributes}")
        if self.endpoint:
            log_detailed(f"  → Endpoint: {self.endpoint}")
        
        start_time = time.time()
        decrement_counter(name, by=by, attributes=attributes or {})
        duration = time.time() - start_time
        
        log_detailed(f"✓ Counter decremented successfully (took {duration:.3f}s)")
        log_detailed("✓ SDK accepted metric, will export in background")
