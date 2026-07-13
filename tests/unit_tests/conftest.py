# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import pytest
import threading
import sys

def pytest_sessionfinish(session, exitstatus):
    """Force immediate shutdown of all daemon threads to prevent 30s hang."""
    # Get all OTEL daemon threads
    otel_threads = [
        t for t in threading.enumerate()
        if t.daemon and 'Otel' in t.name
    ]

    if otel_threads:
        # Set a very short timeout for Python's shutdown
        # This prevents Python from waiting 30 seconds for daemon threads
        import os
        os._exit(exitstatus)
