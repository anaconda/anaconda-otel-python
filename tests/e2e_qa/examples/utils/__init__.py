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
    setup_python_path,
    load_environment,
    create_basic_config,
    create_basic_attributes,
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
)

# Import from telemetry_utils
from .telemetry_utils import (
    flush_telemetry,
    flush_metrics,
    flush_traces,
    flush_logs,
)

__all__ = [
    # Config utils
    'setup_python_path',
    'load_environment',
    'create_basic_config',
    'create_basic_attributes',
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
    # Telemetry utils
    'flush_telemetry',
    'flush_metrics',
    'flush_traces',
    'flush_logs',
]
