# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0
import sys
sys.path.append("./")

import json, re
from test_files.example_app import simulate_metric

class TestMetricExport:

    def test_metrics(self):
        """Verify metrics appear in console simulate_output."""
        simulate_output = simulate_metric()
        assert 'http_requests_total' in simulate_output, "Counter metric 'http_requests_total' not found in simulate_output"
        assert 'request_duration_seconds' in simulate_output, "Histogram metric 'request_duration_seconds' not found in simulate_output"
        assert 'request_queue_depth' in simulate_output, "Gauge metric 'request_queue_depth' not found in simulate_output"
        assert re.search(r'method.*GET', simulate_output), "Counter attribute 'method: GET' not found"
        assert re.search(r'endpoint.*/api/data', simulate_output), "Metric attribute 'endpoint: /api/data' not found"

    def test_gauge_exports_as_gauge(self):
        """Verify the gauge exports as an OTel gauge, not as a sum or a histogram.

        Substring checks on the payload cannot tell these apart, so assert on the shape of the
        exported data: a gauge carries only last-value data points, while a sum carries
        'is_monotonic'/'aggregation_temporality' and a histogram carries bucket counts.
        """
        payload = json.loads(simulate_metric())
        exported = {
            metric['name']: metric
            for resource_metric in payload['resource_metrics']
            for scope_metric in resource_metric['scope_metrics']
            for metric in scope_metric['metrics']
        }

        gauge = exported['request_queue_depth']
        assert 'is_monotonic' not in gauge['data'], "Gauge exported as a sum, not a gauge"
        assert 'aggregation_temporality' not in gauge['data'], "Gauge exported with a sum/histogram temporality"

        data_points = gauge['data']['data_points']
        assert len(data_points) == 1, f"Expected a single gauge data point, got {len(data_points)}"
        assert 'bucket_counts' not in data_points[0], "Gauge exported as a histogram, not a gauge"
        assert isinstance(data_points[0]['value'], (int, float)), "Gauge data point is missing a numeric last value"
        assert data_points[0]['attributes']['endpoint'] == '/api/data'

        # Sanity-check the contrast so this test fails if 'gauge' were ever wired to another instrument.
        assert 'is_monotonic' in exported['http_requests_total']['data'], "Counter no longer exports as a sum"
        assert 'bucket_counts' in exported['request_duration_seconds']['data']['data_points'][0], \
            "Histogram no longer exports bucket counts"
