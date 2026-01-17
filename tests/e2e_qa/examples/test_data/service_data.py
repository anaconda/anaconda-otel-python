# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

"""
Service-related test data constants

Contains service names, versions, environments, and platform identifiers
used across all examples.
"""

from enum import Enum


class ServiceName(str, Enum):
    """Service names for each example"""
    EXAMPLE_01 = 'example-01-all-signals'
    EXAMPLE_02 = 'example-02-metrics-only'
    EXAMPLE_03 = 'example-03-default'
    EXAMPLE_04 = 'example-04-selective'
    EXAMPLE_05 = 'example-05-complete'
    EXAMPLE_06 = 'example-06-env-based'
    CONFIG_EXAMPLES = 'config-examples-service'
    ATTRIBUTES_EXAMPLES = 'attributes-examples-service'


class ServiceVersion(str, Enum):
    """Service versions"""
    DEFAULT = '1.0.0'
    V2 = '2.0.0'
    V2_1 = '2.1.0'
    V3_2_1 = '3.2.1'


class Environment(str, Enum):
    """Environment values"""
    EMPTY = ''
    TEST = 'test'
    DEVELOPMENT = 'development'
    STAGING = 'staging'
    PRODUCTION = 'production'


class Platform(str, Enum):
    """Platform identifiers"""
    CONDA = 'conda'
    KUBERNETES = 'kubernetes'
    DOCKER = 'docker'
