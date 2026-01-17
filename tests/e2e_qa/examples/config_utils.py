# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Configuration Utilities for E2E QA Examples

This module provides shared utilities for loading environment configuration
and setting up telemetry across all examples.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from anaconda.opentelemetry import Configuration, ResourceAttributes


# Environment to endpoint mapping
# Note: Use WARP endpoints when connected to WARP VPN
ENDPOINTS = {
    'staging-internal': 'https://metrics.stage.anacondaconnect.com/v1/metrics',  # Behind WARP
    'staging-internal-gha': 'https://metrics.stage.internal.anacondaconnect.com/v1/metrics',  # GitHub Actions
    'staging-public': 'https://metrics.stage-oauth.anacondaconnect.com/v1/metrics',
    'production-external': 'https://metrics.anaconda.com/v1/metrics',
    'production-internal': 'https://metrics.internal.anaconda.com/v1/metrics',
}


def load_environment():
    """
    Load environment variables from .env file.
    
    Returns:
        tuple: (environment_name, endpoint_url, use_console_exporter)
    """
    # Find and load .env file from e2e_qa directory
    e2e_qa_dir = Path(__file__).parent.parent
    env_file = e2e_qa_dir / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
    else:
        print(f"⚠️  Warning: .env file not found at {env_file}")
        print("   Using default values. Copy env.example to .env to configure.")
    
    # Get configuration from environment
    environment = os.getenv('OTEL_ENVIRONMENT', 'staging-internal')
    custom_endpoint = os.getenv('OTEL_ENDPOINT')
    use_console = os.getenv('OTEL_CONSOLE_EXPORTER', 'true').lower() in ['true', 'yes', '1']
    
    # Use custom endpoint if provided, otherwise use environment mapping
    endpoint = custom_endpoint or ENDPOINTS.get(environment)
    
    if not endpoint:
        raise ValueError(f"Unknown environment: {environment}. Valid options: {list(ENDPOINTS.keys())}")
    
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
    # Map environment name to valid ResourceAttributes environment value
    env_mapping = {
        'staging-internal': 'staging',
        'staging-public': 'staging',
        'production-external': 'production',
        'production-internal': 'production',
    }
    environment = env_mapping.get(env_name, 'development')
    
    attrs.set_attributes(
        otel_environment=env_name,  # Store original as custom attribute
        test_type='e2e-qa'
    )
    attrs.environment = environment  # Set valid environment value
    
    # Add any additional attributes
    if kwargs:
        attrs.set_attributes(**kwargs)
    
    return attrs


def print_example_header(title: str, description: str = ""):
    """Print a formatted example header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)
    if description:
        print(f"  {description}")
        print("-" * 70)


def print_example_section(section_name: str):
    """Print a formatted section header."""
    print(f"\n--- {section_name} ---")


def print_success(message: str):
    """Print a success message."""
    print(f"✓ {message}")


def print_info(message: str):
    """Print an info message."""
    print(f"  {message}")


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
