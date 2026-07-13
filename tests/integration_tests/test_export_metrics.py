# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0
import sys
sys.path.append("./")

import re
from test_files.example_app import simulate_metric

class TestMetricExport:

    def test_metrics(self):
        """Verify metrics appear in console simulate_output."""
        simulate_output = simulate_metric()
        assert 'http_requests_total' in simulate_output, "Counter metric 'http_requests_total' not found in simulate_output"
        assert 'request_duration_seconds' in simulate_output, "Histogram metric 'request_duration_seconds' not found in simulate_output"
        assert re.search(r'method.*GET', simulate_output), "Counter attribute 'method: GET' not found"
        assert re.search(r'endpoint.*/api/data', simulate_output), "Metric attribute 'endpoint: /api/data' not found"
