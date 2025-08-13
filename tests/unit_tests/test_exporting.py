# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0
import sys
sys.path.append("./")

import re
from test_files.example_app import simulate_metric, simulate_log, simulate_trace

class TestSignalExport:

    def test_metrics(self):
        """Verify metrics appear in console simulate_output."""
        simulate_output = simulate_metric()
        assert 'http_requests_total' in simulate_output, "Counter metric 'http_requests_total' not found in simulate_output"
        assert 'request_duration_seconds' in simulate_output, "Histogram metric 'request_duration_seconds' not found in simulate_output"
        assert re.search(r'method.*GET', simulate_output), "Counter attribute 'method: GET' not found"
        assert re.search(r'endpoint.*/api/data', simulate_output), "Metric attribute 'endpoint: /api/data' not found"

    def test_traces(self):
        """Verify traces appear in console simulate_output."""
        simulate_output = simulate_trace()
        assert 'user_request' in simulate_output, "Span name 'user_request' not found in simulate_output"
        assert re.search(r'request\.type', simulate_output), "Span attribute 'request.type' not found"
        assert 'api_call' in simulate_output, "Span attribute value 'api_call' not found"

    def test_logs(self):
        """Verify logs appear in console simulate_output."""
        simulate_output = simulate_log()
        assert 'Initialized telemetry for integration test' in simulate_output, "Test log message not found in simulate_output"
        assert 'test-service' in simulate_output, "Service name 'test-service' not found in simulate_output"
        assert 'severity_text' in simulate_output, "Log field 'severity_text' not found in simulate_output"
        assert 'severity_number' in simulate_output, "Log field 'severity_number' not found in simulate_output"