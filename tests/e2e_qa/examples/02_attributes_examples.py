# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Resource Attributes Examples

This module demonstrates how to create and configure ResourceAttributes
for the Anaconda OpenTelemetry SDK.
"""

from anaconda.opentelemetry import ResourceAttributes
from config_utils import (
    print_example_header,
    print_example_section,
    print_success,
    print_info
)


def example_01_basic_attributes():
    """Example 1: Create basic ResourceAttributes with required fields"""
    print_example_section("Example 1: Basic ResourceAttributes")
    print_info("Create ResourceAttributes with required service_name and service_version")
    
    # Create basic attributes (only required fields)
    attrs = ResourceAttributes(
        service_name="my-service",
        service_version="1.0.0"
    )
    
    print_success("ResourceAttributes created")
    print_info(f"Service name: {attrs.service_name}")
    print_info(f"Service version: {attrs.service_version}")
    print_info(f"SDK version (auto): {attrs.client_sdk_version}")
    print_info(f"Schema version (auto): {attrs.schema_version}")
    
    return attrs


def example_02_optional_fields():
    """Example 2: Use optional fields"""
    print_example_section("Example 2: Optional Fields")
    print_info("Add optional fields like platform, hostname, environment")
    
    # Create attributes with optional fields
    attrs = ResourceAttributes(
        service_name="my-service",
        service_version="1.0.0",
        platform="conda",
        hostname="my-laptop",
        environment="development"
    )
    
    print_success("ResourceAttributes with optional fields created")
    print_info(f"Platform: {attrs.platform}")
    print_info(f"Hostname: {attrs.hostname}")
    print_info(f"Environment: {attrs.environment}")
    
    return attrs


def example_03_auto_populated_fields():
    """Example 3: Auto-populated fields"""
    print_example_section("Example 3: Auto-Populated Fields")
    print_info("Some fields are automatically populated if not provided")
    
    # Create attributes without optional fields - they'll be auto-populated
    attrs = ResourceAttributes(
        service_name="my-service",
        service_version="1.0.0"
    )
    
    print_success("ResourceAttributes created with auto-populated fields")
    print_info(f"OS type (auto): {attrs.os_type}")
    print_info(f"OS version (auto): {attrs.os_version}")
    print_info(f"Python version (auto): {attrs.python_version}")
    print_info(f"Hostname (auto): {attrs.hostname}")
    
    return attrs


def example_04_set_attributes_method():
    """Example 4: Use set_attributes() to add custom attributes"""
    print_example_section("Example 4: set_attributes() Method")
    print_info("Add custom attributes after creation using set_attributes()")
    
    # Create basic attributes
    attrs = ResourceAttributes(
        service_name="my-service",
        service_version="1.0.0"
    )
    
    # Add custom attributes
    attrs.set_attributes(
        team="data-science",
        project="ml-pipeline",
        region="us-west-2"
    )
    
    print_success("Custom attributes added")
    print_info("Custom attributes stored in 'parameters' dict:")
    print_info(f"  team: {attrs.parameters.get('team')}")
    print_info(f"  project: {attrs.parameters.get('project')}")
    print_info(f"  region: {attrs.parameters.get('region')}")
    
    return attrs


def example_05_update_existing_attributes():
    """Example 5: Update existing attributes"""
    print_example_section("Example 5: Update Existing Attributes")
    print_info("Modify existing attributes using set_attributes()")
    
    # Create attributes
    attrs = ResourceAttributes(
        service_name="my-service",
        service_version="1.0.0",
        environment="development"
    )
    
    print_info(f"Initial environment: {attrs.environment}")
    
    # Update environment
    attrs.set_attributes(environment="staging")
    
    print_success("Attribute updated")
    print_info(f"Updated environment: {attrs.environment}")
    
    return attrs


def example_06_environment_specific_attributes():
    """Example 6: Environment-specific attributes"""
    print_example_section("Example 6: Environment-Specific Attributes")
    print_info("Add attributes that identify the deployment environment")
    
    # Create attributes with environment information
    attrs = ResourceAttributes(
        service_name="web-api",
        service_version="2.1.0",
        environment="production",
        platform="kubernetes"
    )
    
    # Add deployment-specific attributes
    attrs.set_attributes(
        deployment_environment="production",
        deployment_region="us-east-1",
        deployment_cluster="prod-cluster-01"
    )
    
    print_success("Environment-specific attributes configured")
    print_info(f"Environment: {attrs.environment}")
    print_info(f"Platform: {attrs.platform}")
    print_info("Deployment attributes:")
    print_info(f"  Region: {attrs.parameters.get('deployment_region')}")
    print_info(f"  Cluster: {attrs.parameters.get('deployment_cluster')}")
    
    return attrs


def example_07_user_identification():
    """Example 7: User identification"""
    print_example_section("Example 7: User Identification")
    print_info("Add user_id for tracking user-specific telemetry")
    
    # Create attributes with user_id
    attrs = ResourceAttributes(
        service_name="user-app",
        service_version="1.0.0",
        user_id="user_12345"
    )
    
    print_success("User identification configured")
    print_info(f"User ID: {attrs.user_id}")
    print_info("Note: user_id is handled specially and not included in resource attributes")
    
    return attrs


def example_08_complete_attributes():
    """Example 8: Complete attributes configuration"""
    print_example_section("Example 8: Complete Attributes")
    print_info("Combine all attribute types for comprehensive configuration")
    
    # Create comprehensive attributes
    attrs = ResourceAttributes(
        service_name="analytics-service",
        service_version="3.2.1",
        platform="conda",
        environment="production",
        user_id="analyst_001"
    )
    
    # Add custom attributes
    attrs.set_attributes(
        team="analytics",
        project="user-behavior-analysis",
        deployment_region="us-west-2",
        deployment_cluster="prod-analytics-01",
        cost_center="engineering",
        data_classification="confidential"
    )
    
    print_success("Complete attributes configuration created")
    print_info("Standard attributes:")
    print_info(f"  Service: {attrs.service_name} v{attrs.service_version}")
    print_info(f"  Platform: {attrs.platform}")
    print_info(f"  Environment: {attrs.environment}")
    print_info(f"  User ID: {attrs.user_id}")
    print_info(f"Custom attributes: {len(attrs.parameters)} attributes")
    
    return attrs


def example_09_validation():
    """Example 9: Attribute validation"""
    print_example_section("Example 9: Attribute Validation")
    print_info("Demonstrate attribute validation rules")
    
    # Valid service names (alphanumeric, dots, dashes, underscores, max 30 chars)
    valid_names = [
        "my-service",
        "my_service",
        "my.service",
        "service123",
        "Service-Name_v1.0"
    ]
    
    print_info("Valid service name patterns:")
    for name in valid_names:
        try:
            attrs = ResourceAttributes(
                service_name=name,
                service_version="1.0.0"
            )
            print_info(f"  ✓ '{name}' - valid")
        except ValueError as e:
            print_info(f"  ✗ '{name}' - invalid: {e}")
    
    # Valid environment values
    valid_environments = ["", "test", "development", "staging", "production"]
    
    print_info("\nValid environment values:")
    for env in valid_environments:
        attrs = ResourceAttributes(
            service_name="test-service",
            service_version="1.0.0",
            environment=env
        )
        display_env = env if env else "(empty string)"
        print_info(f"  ✓ '{display_env}' - valid")
    
    print_success("Validation examples completed")
    
    return attrs


def run_all_examples():
    """Run all resource attributes examples"""
    print_example_header(
        "Resource Attributes Examples",
        "Demonstrating ResourceAttributes class and its methods"
    )
    
    # Run examples
    example_01_basic_attributes()
    example_02_optional_fields()
    example_03_auto_populated_fields()
    example_04_set_attributes_method()
    example_05_update_existing_attributes()
    example_06_environment_specific_attributes()
    example_07_user_identification()
    example_08_complete_attributes()
    example_09_validation()
    
    print("\n" + "=" * 70)
    print_success("All resource attributes examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_all_examples()
