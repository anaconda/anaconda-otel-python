# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Resource attribute test data constants

Contains custom attributes, deployment attributes, user IDs, and other
resource-level metadata used in examples.
"""

from enum import Enum


class CustomAttributes(Enum):
    """Custom attributes for examples"""
    EXAMPLE_01 = {
        'example': 'all_signals',
        'test_type': 'e2e-qa',
    }
    EXAMPLE_02 = {
        'example': 'metrics_only',
        'test_type': 'e2e-qa',
    }
    EXAMPLE_03 = {
        'example': 'default_initialization',
        'test_type': 'e2e-qa',
    }
    EXAMPLE_04 = {
        'example': 'selective_signals',
        'test_type': 'e2e-qa',
    }
    EXAMPLE_COMPLETE = {
        'example': 'complete_initialization',
        'test_type': 'e2e-qa',
    }
    EXAMPLE_ENV_BASED = {
        'test_type': 'e2e-qa',
    }
    EXAMPLE_07 = {
        'example': 'flush_test',
        'test_type': 'e2e-qa',
    }
    TEAM_PROJECT = {
        'team': 'data-science',
        'project': 'ml-pipeline',
        'region': 'us-west-2',
    }
    ANALYTICS_TEAM = {
        'team': 'analytics',
        'project': 'user-behavior-analysis',
        'cost_center': 'engineering',
        'data_classification': 'confidential',
    }


class TestType(str, Enum):
    """Test type identifiers"""
    E2E_QA = 'e2e-qa'
    UNIT_TEST = 'unit-test'
    INTEGRATION_TEST = 'integration-test'


class AutoDetectedAttributes(Enum):
    """Auto-detected attributes for documentation purposes"""
    STANDARD = {
        "os.type": "Darwin/Linux/Windows (auto-detected)",
        "python.version": "3.x.x (auto-detected)",
        "client.sdk.version": "0.0.0.devbuild",
        "schema.version": "0.3.0"
    }


class DeploymentAttributes(Enum):
    """Deployment-specific attributes"""
    US_EAST_PROD = {
        'deployment_environment': 'production',
        'deployment_region': 'us-east-1',
        'deployment_cluster': 'prod-cluster-01',
    }
    US_WEST_STAGING = {
        'deployment_environment': 'staging',
        'deployment_region': 'us-west-2',
        'deployment_cluster': 'staging-cluster-01',
    }
    ANALYTICS_PROD = {
        'deployment_region': 'us-west-2',
        'deployment_cluster': 'prod-analytics-01',
    }


class UserId(str, Enum):
    """User IDs for testing"""
    TEST_USER_1 = 'user_12345'
    ANALYST_1 = 'analyst_001'
    DEVELOPER_1 = 'dev_001'


class Hostname(str, Enum):
    """Hostname identifiers for testing"""
    MY_LAPTOP = 'my-laptop'
    DEV_WORKSTATION = 'dev-workstation'
    TEST_SERVER = 'test-server'
