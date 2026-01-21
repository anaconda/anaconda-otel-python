# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Utilities Package for E2E QA Examples

This package provides shared utilities for E2E QA examples including:
- Configuration management (config_utils)
- Print/output formatting (print_utils)
- Telemetry operations (telemetry_utils)
"""

# Import from config_utils
from .config_utils import (
    # Enums
    EndpointType,
    EndpointEnvVar,
    # Functions
    load_environment,
    get_session_id,
    validate_environment,
)

# Import from print_utils
from .print_utils import (
    # Header and Footer
    print_header,
    print_footer,
    print_section,
    # Basic prints
    print_success,
    print_info,
    print_code,
    # Detailed logging
    log_detailed,
    # Specialized prints
    print_environment_config,
    print_resource_attributes,
    print_metric_info,
    print_backend_validation,
    print_sdk_commands_summary,
    print_flush_status,
    print_initialization_status,
    print_validation_info,
    # Backward compatibility aliases
    print_example_header,
    print_example_section,
    # Error detection and reporting
    extract_http_errors,
    process_subprocess_output,
    run_example_subprocess,
    print_examples_summary,
    print_error_highlights,
)

# Import from sdk_operations
from .sdk_operations import (
    SdkOperations,
)

__all__ = [
    # Config utils - Enums
    'EndpointType',
    'EndpointEnvVar',
    # Config utils - Functions
    'load_environment',
    'get_session_id',
    'validate_environment',
    # Print utils - Headers/Footers
    'print_header',
    'print_footer',
    'print_section',
    # Print utils - Basic
    'print_success',
    'print_info',
    'print_code',
    # Print utils - Detailed logging
    'log_detailed',
    # Print utils - Specialized
    'print_environment_config',
    'print_resource_attributes',
    'print_metric_info',
    'print_backend_validation',
    'print_sdk_commands_summary',
    'print_flush_status',
    'print_initialization_status',
    'print_validation_info',
    # Print utils - Backward compatibility
    'print_example_header',
    'print_example_section',
    # Print utils - Error detection and reporting
    'extract_http_errors',
    'process_subprocess_output',
    'run_example_subprocess',
    'print_examples_summary',
    'print_error_highlights',
    # SDK operations
    'SdkOperations',
]
