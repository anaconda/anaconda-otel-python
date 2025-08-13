# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys
sys.path.append("./")

import logging

from anaconda_opentelemetry.attributes import ResourceAttributes
from anaconda_opentelemetry.config import Configuration
from anaconda_opentelemetry.signals import (
    initialize_telemetry,
    increment_counter
)

# Configure logging
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

class IntegrationTestApp:
    """Example application that generates various telemetry signals. Simulates metric on init."""

    def export_metric(self) -> None:

        # Increment request counter
        increment_counter(
            "integration_tests",
            by=1        )
    
    def __init__(
            self,
            service_name: str = "test-service",
            service_version: str = "0.1.0"
    ):
        """
        Initialize the example app with telemetry. Auth token and endpoint must be environment variables.
        
        Args:
            service_name: Name of the service creating telemetry
            service_version: Version of service creating telemetry
        """

        self.service_name = service_name
        # initialize required classes
        attrs = ResourceAttributes(service_name, service_version)
        config = Configuration(default_endpoint="http://localhost:4000")

        attrs.set_attributes(test="foo", environment="test")
        
        # initialize package
        initialize_telemetry(config, attrs, signal_types=["metrics"])

        # simulate metric
        self.export_metric()