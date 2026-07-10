# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0
import sys
sys.path.append("./")

from test_files.example_app import simulate_log

class TestLogExport:

    def test_logs(self):
        """Verify logs appear in console simulate_output."""
        simulate_output = simulate_log()
        assert 'Initialized telemetry for integration test' in simulate_output, "Test log message not found in simulate_output"
        assert 'test-service' in simulate_output, "Service name 'test-service' not found in simulate_output"
        assert 'severity_text' in simulate_output, "Log field 'severity_text' not found in simulate_output"
        assert 'severity_number' in simulate_output, "Log field 'severity_number' not found in simulate_output"
