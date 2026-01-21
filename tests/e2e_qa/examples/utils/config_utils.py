# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Configuration Utilities for E2E QA Examples

This module provides shared utilities for loading environment configuration
and setting up telemetry across all examples.
"""

import os
import sys
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
from anaconda.opentelemetry import Configuration, ResourceAttributes
# Import print utilities for backward compatibility
from .print_utils import (
    print_example_header,
    print_example_section,
    print_success,
    print_info,
    print_code,
    print_validation_info
)

class EndpointType(Enum):
    """Enum for OpenTelemetry signal endpoint types."""
    DEFAULT = 'default'
    LOGGING = 'logging'
    METRICS = 'metrics'
    TRACING = 'tracing'


class EndpointEnvVar(Enum):
    """Environment variable names for OpenTelemetry endpoints."""
    DEFAULT = 'OTEL_ENDPOINT'
    LOGGING = 'OTEL_LOGGING_ENDPOINT'
    METRICS = 'OTEL_METRICS_ENDPOINT'
    TRACING = 'OTEL_TRACING_ENDPOINT'

def load_environment():
    """
    Load environment variables from .env file.
    
    Returns:
        tuple: (environment_name, endpoint_url, use_console_exporter, endpoints_dict)
        
        endpoints_dict contains:
            - 'default': default endpoint (required)
            - 'logging': logging-specific endpoint (optional)
            - 'metrics': metrics-specific endpoint (optional)
            - 'tracing': tracing-specific endpoint (optional)
    
    Environment variables loaded from .env:
        - OTEL_ENVIRONMENT: Environment name (staging, production, etc.)
        - OTEL_ENDPOINT: Default endpoint URL
        - OTEL_CONSOLE_EXPORTER: Enable console output (true/false)
        - OTEL_*_ENDPOINT: Signal-specific endpoints (optional)
    """
    # Find and load .env file from e2e_qa directory
    # Path: examples/utils/config_utils.py -> examples/utils -> examples -> e2e_qa
    e2e_qa_dir = Path(__file__).parent.parent.parent
    env_file = e2e_qa_dir / '.env'
    
    if env_file.exists():
        load_dotenv(env_file, override=True)
    else:
        print(f"⚠️  Warning: .env file not found at {env_file}")
        print("   Using default values.")
    
    # Get configuration from environment
    environment = os.getenv('OTEL_ENVIRONMENT', 'staging')
    endpoint = os.getenv(EndpointEnvVar.DEFAULT.value)
    use_console = os.getenv('OTEL_CONSOLE_EXPORTER', 'true').lower() in ['true', 'yes', '1']
    
    if not endpoint:
        raise ValueError(
            f"{EndpointEnvVar.DEFAULT.value} is required. Please set it in your .env file.\n"
            "See env.example for reference."
        )
    
    # Load signal-specific endpoints (optional)
    endpoints = {
        EndpointType.DEFAULT.value: endpoint,
        EndpointType.LOGGING.value: os.getenv(EndpointEnvVar.LOGGING.value),
        EndpointType.METRICS.value: os.getenv(EndpointEnvVar.METRICS.value),
        EndpointType.TRACING.value: os.getenv(EndpointEnvVar.TRACING.value),
    }
    
    return environment, endpoint, use_console, endpoints


def get_session_id(attrs):
    """
    Get the session ID from ResourceAttributes.
    
    Args:
        attrs: ResourceAttributes object
    
    Returns:
        str: Session ID or None if not available
    """
    try:
        # Try to get session_id attribute if it exists
        if hasattr(attrs, 'session_id'):
            return attrs.session_id
        # Try to get from parameters dict
        if hasattr(attrs, 'parameters') and isinstance(attrs.parameters, dict):
            return attrs.parameters.get('session_id')
    except:
        pass
    return None


def validate_environment():
    """
    Validate environment configuration and warn if using production.
    
    Returns:
        str: The environment name
    """
    environment, endpoint, _, _ = load_environment()
    
    print_info(f"Environment: {environment}")
    print_info(f"Endpoint: {endpoint}")
    
    # Warn if using production
    if environment.startswith('production'):
        print("\n⚠️  WARNING: Using production environment!")
        print("   Only send real production data to production endpoints.")
        response = input("   Continue? (yes/no): ")
        if response.lower() != 'yes':
            raise ValueError("Production environment usage cancelled")
    
    return environment
