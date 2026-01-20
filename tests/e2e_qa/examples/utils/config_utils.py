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
from pathlib import Path
from dotenv import load_dotenv
from anaconda.opentelemetry import Configuration, ResourceAttributes


def setup_python_path():
    """
    Setup Python path to enable imports from the examples directory.
    
    NOTE: This function is kept for backward compatibility but is generally
    not needed. The anaconda.opentelemetry package is installed via 
    'pip install -e .' and is available globally. Scripts only need to add
    the examples directory to sys.path for local utils/test_data imports.
    
    Adds to sys.path (if not already present):
    - Examples directory (for utils and test_data imports)
    
    Returns:
        Path: examples_dir as Path object
    """
    # Determine the examples directory based on this file's location
    # Path: examples/utils/config_utils.py -> examples/utils -> examples
    current_file = Path(__file__)
    examples_dir = current_file.parent.parent  # Go up to examples directory
    
    # Add examples directory to path (for utils and test_data imports)
    if str(examples_dir) not in sys.path:
        sys.path.insert(0, str(examples_dir))
    
    return examples_dir

# Import print utilities for backward compatibility
from .print_utils import (
    print_example_header,
    print_example_section,
    print_success,
    print_info,
    print_code,
    print_validation_info
)


def load_environment():
    """
    Load environment variables from .env file.
    
    Returns:
        tuple: (environment_name, endpoint_url, use_console_exporter)
    """
    # Find and load .env file from e2e_qa directory
    # Path: examples/utils/config_utils.py -> examples/utils -> examples -> e2e_qa
    e2e_qa_dir = Path(__file__).parent.parent.parent
    env_file = e2e_qa_dir / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
    else:
        print(f"⚠️  Warning: .env file not found at {env_file}")
        print("   Using default values.")
    
    # Get configuration from environment
    environment = os.getenv('OTEL_ENVIRONMENT', 'staging')
    endpoint = os.getenv('OTEL_ENDPOINT')
    use_console = os.getenv('OTEL_CONSOLE_EXPORTER', 'true').lower() in ['true', 'yes', '1']
    
    if not endpoint:
        raise ValueError(
            "OTEL_ENDPOINT is required. Please set it in your .env file.\n"
            "See env.example for reference."
        )
    
    return environment, endpoint, use_console


def create_basic_config(endpoint: str = None, use_console: bool = True):
    """
    Create a basic Configuration object.
    
    Args:
        endpoint: Optional endpoint URL. If not provided, loads from environment.
        use_console: Whether to enable console exporter for debugging.
    
    Returns:
        Configuration: Configured Configuration object
    """
    if endpoint is None:
        _, endpoint, use_console = load_environment()
    
    config = Configuration(default_endpoint=endpoint)
    
    if use_console:
        config.set_console_exporter(use_console=True)
    
    return config


def create_basic_attributes(service_name: str = "e2e-qa-examples", 
                            service_version: str = "1.0.0",
                            **kwargs):
    """
    Create basic ResourceAttributes with common settings.
    
    Args:
        service_name: Name of the service
        service_version: Version of the service
        **kwargs: Additional attributes to set
    
    Returns:
        ResourceAttributes: Configured ResourceAttributes object
    """
    attrs = ResourceAttributes(
        service_name=service_name,
        service_version=service_version
    )
    
    # Add environment information
    env_name, _, _ = load_environment()
    
    attrs.set_attributes(
        otel_environment=env_name,  # Store environment name as custom attribute
        test_type='e2e-qa'
    )
    attrs.environment = env_name  # Set environment value
    
    # Add any additional attributes
    if kwargs:
        attrs.set_attributes(**kwargs)
    
    return attrs


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
    environment, endpoint, _ = load_environment()
    
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


# Export all utilities for convenience
__all__ = [
    'setup_python_path',
    'load_environment',
    'create_basic_config',
    'create_basic_attributes',
    'get_session_id',
    'validate_environment',
    'print_example_header',
    'print_example_section',
    'print_success',
    'print_info',
    'print_code',
    'print_validation_info',
]
