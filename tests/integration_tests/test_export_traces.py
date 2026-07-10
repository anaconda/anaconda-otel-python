# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0
import sys
sys.path.append("./")

import re
from test_files.example_app import simulate_trace

class TestTraceExport:

    def test_traces(self):
        """Verify traces appear in console simulate_output."""
        simulate_output = simulate_trace()
        assert 'user_request' in simulate_output, "Span name 'user_request' not found in simulate_output"
        assert re.search(r'request\.type', simulate_output), "Span attribute 'request.type' not found"
        assert 'api_call' in simulate_output, "Span attribute value 'api_call' not found"
