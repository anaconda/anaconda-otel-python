#!/usr/bin/env python3
"""
Resource Attributes Examples

This module demonstrates how to create and configure ResourceAttributes
for the Anaconda OpenTelemetry SDK.
"""

from utils import (
    print_example_header,
    print_example_section,
    print_success,
    print_info,
    SdkOperations
)
from test_data import (
    ServiceName,
    ServiceVersion,
    Environment,
    Platform,
    CustomAttributes,
    DeploymentAttributes,
    UserId,
    Hostname
)


def example_01_basic_attributes():
    """Example 1: Create basic ResourceAttributes with required fields"""
    print_example_section("Example 1: Basic ResourceAttributes")
    print_info("Create ResourceAttributes with required service_name and service_version")
    
    # Create basic attributes (only required fields)
    sdk = SdkOperations(show_code=False)
    service_name = ServiceName.ATTRIBUTES_EXAMPLES.value
    service_version = ServiceVersion.DEFAULT.value
    attrs = sdk.create_attributes(
        service_name=service_name,
        service_version=service_version
    )
    
    return attrs


def example_02_optional_fields():
    """Example 2: Use optional fields"""
    print_example_section("Example 2: Optional Fields")
    print_info("Add optional fields like platform, hostname, environment")
    
    # Create attributes with optional fields
    sdk = SdkOperations(show_code=False)
    attrs = sdk.create_attributes(
        service_name=ServiceName.ATTRIBUTES_EXAMPLES.value,
        service_version=ServiceVersion.DEFAULT.value,
        platform=Platform.CONDA.value,
        hostname=Hostname.MY_LAPTOP.value,
        environment=Environment.DEVELOPMENT.value
    )
    
    return attrs


def example_03_auto_populated_fields():
    """Example 3: Auto-populated fields"""
    print_example_section("Example 3: Auto-Populated Fields")
    print_info("Some fields are automatically populated if not provided")
    
    # Create attributes without optional fields - they'll be auto-populated
    sdk = SdkOperations(show_code=False)
    attrs = sdk.create_attributes(
        service_name=ServiceName.ATTRIBUTES_EXAMPLES.value,
        service_version=ServiceVersion.DEFAULT.value
    )
    
    return attrs


def example_04_set_attributes_method():
    """Example 4: Use set_attributes() to add custom attributes"""
    print_example_section("Example 4: set_attributes() Method")
    print_info("Add custom attributes after creation using set_attributes()")
    
    # Create basic attributes
    sdk = SdkOperations(show_code=False)
    attrs = sdk.create_attributes(
        service_name=ServiceName.ATTRIBUTES_EXAMPLES.value,
        service_version=ServiceVersion.DEFAULT.value
    )
    
    # Add custom attributes
    sdk.set_custom_attributes(attrs, **CustomAttributes.TEAM_PROJECT.value)
    
    return attrs


def example_05_update_existing_attributes():
    """Example 5: Update existing attributes"""
    print_example_section("Example 5: Update Existing Attributes")
    print_info("Modify existing attributes using set_attributes()")
    
    # Create attributes
    sdk = SdkOperations(show_code=False)
    attrs = sdk.create_attributes(
        service_name=ServiceName.ATTRIBUTES_EXAMPLES.value,
        service_version=ServiceVersion.DEFAULT.value,
        environment=Environment.DEVELOPMENT.value
    )
    
    print_info(f"Initial environment: {attrs.environment}")
    
    # Update environment
    sdk.set_custom_attributes(attrs, environment=Environment.STAGING.value)
    
    print_info(f"Updated environment: {attrs.environment}")
    
    return attrs


def example_06_environment_specific_attributes():
    """Example 6: Environment-specific attributes"""
    print_example_section("Example 6: Environment-Specific Attributes")
    print_info("Add attributes that identify the deployment environment")
    
    # Create attributes with environment information
    sdk = SdkOperations(show_code=False)
    attrs = sdk.create_attributes(
        service_name=ServiceName.ATTRIBUTES_EXAMPLES.value,
        service_version=ServiceVersion.V2_1.value,
        environment=Environment.PRODUCTION.value,
        platform=Platform.KUBERNETES.value
    )
    
    # Add deployment-specific attributes
    sdk.set_custom_attributes(attrs, **DeploymentAttributes.US_EAST_PROD.value)
    
    return attrs


def example_07_user_identification():
    """Example 7: User identification"""
    print_example_section("Example 7: User Identification")
    print_info("Add user_id for tracking user-specific telemetry")
    
    # Create attributes with user_id
    sdk = SdkOperations(show_code=False)
    attrs = sdk.create_attributes(
        service_name=ServiceName.ATTRIBUTES_EXAMPLES.value,
        service_version=ServiceVersion.DEFAULT.value,
        user_id=UserId.TEST_USER_1.value
    )
    
    return attrs


def example_08_complete_attributes():
    """Example 8: Complete attributes configuration"""
    print_example_section("Example 8: Complete Attributes")
    print_info("Combine all attribute types for comprehensive configuration")
    
    # Create comprehensive attributes
    sdk = SdkOperations(show_code=False)
    attrs = sdk.create_attributes(
        service_name=ServiceName.ATTRIBUTES_EXAMPLES.value,
        service_version=ServiceVersion.V3_2_1.value,
        platform=Platform.CONDA.value,
        environment=Environment.PRODUCTION.value,
        user_id=UserId.ANALYST_1.value
    )
    
    # Add custom attributes
    custom_attrs = {**CustomAttributes.ANALYTICS_TEAM.value, **DeploymentAttributes.ANALYTICS_PROD.value}
    sdk.set_custom_attributes(attrs, **custom_attrs)
    
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
    sdk = SdkOperations(show_code=False)
    for name in valid_names:
        try:
            attrs = sdk.create_attributes(
                service_name=name,
                service_version="1.0.0"
            )
            print_info(f"  [OK] '{name}' - valid")
        except ValueError as e:
            print_info(f"  [FAIL] '{name}' - invalid: {e}")
    
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
