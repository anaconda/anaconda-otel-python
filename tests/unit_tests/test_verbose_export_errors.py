# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys
sys.path.append("./")

import logging
import pytest
from unittest.mock import patch, MagicMock
from anaconda_opentelemetry.config import Configuration as Config
from anaconda_opentelemetry.signals import _suppress_otel_export_errors

class TestVerboseExportErrors:
    def test_verbose_export_errors_default_false(self):
        cfg = Config(default_endpoint="http://localhost:4317")
        assert cfg._get_verbose_export_errors() == False

    def test_suppress_otel_export_errors_silences_logs(self):
        _suppress_otel_export_errors()

        otel_loggers = [
            'opentelemetry.exporter.otlp.proto.grpc.exporter',
            'opentelemetry.exporter.otlp.proto.http.exporter',
            'opentelemetry.exporter.otlp.proto.grpc.metric_exporter',
            'opentelemetry.exporter.otlp.proto.http.metric_exporter',
            'opentelemetry.exporter.otlp.proto.grpc.trace_exporter',
            'opentelemetry.exporter.otlp.proto.http.trace_exporter',
            'opentelemetry.exporter.otlp.proto.grpc._log_exporter',
            'opentelemetry.exporter.otlp.proto.http._log_exporter',
        ]

        for logger_name in otel_loggers:
            logger = logging.getLogger(logger_name)
            assert logger.level == logging.CRITICAL
            assert not logger.isEnabledFor(logging.WARNING)
            assert not logger.isEnabledFor(logging.ERROR)
