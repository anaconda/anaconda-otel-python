# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

import sys, time, json
sys.path.append("./")

from anaconda_opentelemetry.attributes import ResourceAttributes as Attributes
from anaconda_opentelemetry.signals import _AnacondaCommon as AnacondaTelBase
from anaconda_opentelemetry.signals import _AnacondaLogger as AnacondaLogger
from anaconda_opentelemetry.signals import _AnacondaTrace as AnacondaTrace
from anaconda_opentelemetry.signals import _AnacondaMetrics as AnacondaMetrics
from anaconda_opentelemetry.config import Configuration as Config
from anaconda_opentelemetry.signals import AttrDict
from opentelemetry.trace import Span, Tracer
from opentelemetry.metrics import Meter, Histogram
from opentelemetry.sdk.resources import Resource
from opentelemetry.context import Context

from typing import Dict, Callable, Union
import pytest, hashlib, re, logging, os
from unittest.mock import patch, MagicMock


# utility function
def read_config(config_file_path="tests/unit_tests/test_files/config.yaml"):
    if config_file_path.endswith('.yaml') or config_file_path.endswith('.yml'):
        from yaml import safe_load
        with open(config_file_path, 'r') as config_file:
            config_dict = safe_load(config_file)
    else:
        raise ValueError("Unsupported config file format. Only YAML is supported for this test.")
    return config_dict

@pytest.fixture(scope="module", autouse=True)
def setup_mock_logging():
    with patch('logging.getLogger') as mock_getLogger:
        mock_getLogger.return_value = MagicMock()
        mock_getLogger.return_value.level = logging.WARNING
        yield mock_getLogger

class TestAnacondaCommon:

    # class-wide test vars
    # default mock time value that is class wide
    time_patch_value = 1_234_567_899.0
    # name of service
    service_name = "test-service"
    # id of user - must match config file value
    user_id = "user123"

    @pytest.fixture(scope="class")
    def _patch_time(self, request):
        mp = pytest.MonkeyPatch()
        mp.setattr(time, "time", lambda: request.cls.time_patch_value)
        yield
        mp.undo()


    @pytest.fixture(scope="class")
    def AnacondaCommon(self, _patch_time, request) -> AnacondaTelBase:
        os.environ.clear()  # clear previous test environment vars
        config_values = read_config()
        config_dict, attributes = config_values['configs'], config_values['attributes']
        config_dict['entropy'] = "timestamp"  # this value is required and normally initialized by initialize_telemetry()
        config = Config(config_dict=config_dict)

        service_name = "test-service"
        service_version = "1.0.0"
        attributes = Attributes(service_name, service_version)
        attributes.set_attributes(foo="test")
        attributes.user_id == TestAnacondaCommon.user_id
        # initialize class for testing
        instance = AnacondaTelBase(config, attributes)

        return instance

    def test_hash_session_id_with_valid_user_id(self, AnacondaCommon: AnacondaTelBase):
        """
        Tests the hash method with both user_id and entropy_value passed
	    - Checks that method ouptut equals that of hashlib.sha256 output
        """
        # construct mock hash
        ts = int(time.time() * 1e9)  # format timestamp like in class function
        expected_combined = f"{ts}|{AnacondaCommon._resource_attributes['user.id']}|{self.service_name}"
        expected_hash = hashlib.sha256(expected_combined.encode("utf-8")).hexdigest()
        # real hash function call
        AnacondaCommon._hash_session_id(ts)

        assert AnacondaCommon._resource_attributes['session.id'] == expected_hash

    def test_hash_session_id_with_none_user_id(self, AnacondaCommon: AnacondaTelBase):
        """
        Tests the hash method with user_id equal to None and an entropy_value passed
        - Checks that the method correctly handles user_id == None by once again comparing hash output
        """
        # construct mock hash
        user_id = ''
        ts = int(self.time_patch_value * 1e9)  # format timestamp like in class function
        expected_combined = f"{ts}|{user_id}|{self.service_name}"
        expected_hash = hashlib.sha256(expected_combined.encode("utf-8")).hexdigest()
        # real hash function call
        AnacondaCommon._resource_attributes['user.id'] = user_id
        AnacondaCommon._hash_session_id(ts)

        assert AnacondaCommon._resource_attributes['session.id'] == expected_hash

    def test_hash_session_id_with_no_entropy_value(self, AnacondaCommon: AnacondaTelBase):
        """
        - Checks that the method throws a KeyError exception if entropy_value is None
        - Asserted string must match exact Exception argument
        """

        # real hash function call
        with pytest.raises(KeyError) as exception:
            AnacondaCommon._hash_session_id(None)
        assert exception.value.args[0] == 'The entropy key has been removed.'

    def test_hash_output_length(self, AnacondaCommon: AnacondaTelBase):
        """
        - Checks that the sha256 hash output is of length 64
        """
        AnacondaCommon._resource_attributes['user.id'] = 'testuser'
        AnacondaCommon._hash_session_id("timestamp")
        result = AnacondaCommon._resource_attributes['session.id']

        assert isinstance(result, str)
        assert len(result) == 64  # SHA-256 hex digest should be 64 characters

    def test_client_sdk_valid_version(self, AnacondaCommon: AnacondaTelBase):
        """
        Uses regex to check that this value is valid semver
        """
        sdk_version = AnacondaCommon._resource_attributes["client.sdk.version"]
        if sdk_version == '0.0.0.devbuild':
            return
        valid_semver = re.compile(r"^\d+\.\d+\.\d+(?:\.commit\d+)?(?:\+g[0-9a-f]+)?$")

        assert bool(valid_semver.fullmatch(sdk_version))

    def test_schema_valid_version(self, AnacondaCommon: AnacondaTelBase):
        """
        Uses regex to check that this value is valid semver
        """
        schema_version = AnacondaCommon._resource_attributes["schema.version"]
        valid_semver = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")

        assert bool(valid_semver.fullmatch(schema_version))

    def test_resource_attributes(self, AnacondaCommon: AnacondaTelBase):
        """
        - Checks that all required keys exist in resource_attributes
        - Checks that all keys have a value not equal to None
        """
        resource_attributes = AnacondaCommon.resource.attributes

        # Ensure keys and values are str or None
        for k, v in resource_attributes.items():
            assert isinstance(k, str), f"Key {k} is not a string"
            assert isinstance(v, (str, type(None))), f"Value for key '{k}' is not a string or None"

        # Required fields that must have non-None values
        required_common_attributes = [
            "service.name",
            "service.version",
            "client.sdk.version",
            "schema.version",
            "os.type",
            "os.version",
            "python.version",
            "hostname",
            "session.id",
            "environment"
        ]

        for key in required_common_attributes:
            assert key in resource_attributes, f"Missing required key: {key}"
            assert resource_attributes[key] is not None, f"Required key '{key}' has None value"

    def test_create_resource(self, AnacondaCommon: AnacondaTelBase):
        """
        - Checks that the resource created by AnacondaCommon is of type Resource
        """
        assert isinstance(AnacondaCommon.resource, Resource) is True

    def test_json_stringify_on_parameters(self, AnacondaCommon: AnacondaTelBase):
        """
        - Checks that the resource attribute parameters is JSON stringified
        """
        assert AnacondaCommon._resource_attributes['parameters'] == json.dumps({"foo": "test"})


class TestAnacondaLogger:
    instance: AnacondaLogger = None
    # default mock time value that is class wide
    time_patch_value = 1234567899.0

    @patch('opentelemetry.exporter.otlp.proto.http._log_exporter.OTLPLogExporter')
    def test_setup_logging_http(self,  mock_exporter_http: MagicMock):
        """
        - Checks that the OTLPLogExporter from grpc library was called once
        """
        config = Config(default_endpoint="http://localhost:4317").set_console_exporter(False)
        attr = Attributes(service_name='test-name', service_version='0.0.0')

        _ = AnacondaLogger(config, attr)

        mock_exporter_http.assert_called_once()

    @patch('opentelemetry.exporter.otlp.proto.grpc._log_exporter.OTLPLogExporter')
    def test_setup_logging_grpc(self,  mock_exporter_grpc: MagicMock):
        """
        - Checks that the OTLPLogExporter from grpc library was called once
        """
        config = Config(default_endpoint="grpc://localhost:4317").set_console_exporter(False)
        attr = Attributes(service_name='test-name', service_version='0.0.0')
        _ = AnacondaLogger(config, attr)

        mock_exporter_grpc.assert_called_once()

    def test_get_log_level(self):
        """
        Uses a dictionary mappings to check that log levels returned by the method match their expected return value
        """
        test_cases = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "warn": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
            "fatal": logging.CRITICAL,
            "": logging.DEBUG,
            "INFO": logging.INFO,        # uppercase input
            "WaRnInG": logging.WARNING,  # mixed case input
        }
        # with patch('anaconda_opentelemetry.signals._AnacondaLogger._inject_otel_logging'):
        alogger = AnacondaLogger(Config(default_endpoint='http://localhost:4317').set_console_exporter(True),
                                Attributes(service_name='test_name', service_version='0.0.0'))
        for input_str, expected in test_cases.items():
            result = alogger._get_log_level(input_str)
            assert result == expected, f"Expected {expected} for input '{input_str}', got {result}"

class TestAnacondaTrace:
    instance: AnacondaTrace = None
    logger: logging.Logger = None

    @pytest.fixture(scope="class")
    def AnacondaTracer(self) -> AnacondaTrace:
        if TestAnacondaTrace.instance is None:
            TestAnacondaTrace.logger = MagicMock()
            config_values = read_config()
            config_dict = config_values['configs']
            config_dict['entropy'] = "timestamp"  # this value is required and normally initialized by initialize_telemetry()
            config = Config(default_endpoint='http://localhost:4317').set_console_exporter(True)
            attributes = Attributes("test-service", "1.0.0")
            with patch('opentelemetry.trace.set_tracer_provider'),\
                 patch('opentelemetry.sdk.trace.export.ConsoleSpanExporter'):
                TestAnacondaTrace.instance = AnacondaTrace(config, attributes)
                TestAnacondaTrace.instance.use_console_exporters = False
                TestAnacondaTrace.instance.logger = TestAnacondaTrace.logger

        return TestAnacondaTrace.instance

    @pytest.fixture
    def ASpanFactory(self) -> Callable[[AnacondaTrace, str, Dict[str, str]], object]:
        def _make_ASpan(AnacondaTracer, span_name: str ="test-span", attributes: Dict[str, str]={}):
            return AnacondaTracer.get_span(span_name, attributes)
        return _make_ASpan

    def test_ASpan_get_span(
            self,
            AnacondaTracer: AnacondaTrace,
            ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        - Checks that ASpan object returned by the method has a property name of instance string and > length 0
        - Checks that ASpan object returned also has a property span of type Span (otel sdk object)
        - Checks that the trace_id of the Span object is > 0 and < 2**128 (valid trace id)
        - Checks that the span_id of the Span object is > 0 and < 2**64 (valid span id)
        """
        ASpan = ASpanFactory(AnacondaTracer, span_name="test-span", attributes={"test": "1"})

        assert isinstance(ASpan._name, str)
        assert len(ASpan._name) > 0
        assert isinstance(ASpan._span, Span)

        trace_id = ASpan._span.get_span_context().trace_id
        span_id = ASpan._span.get_span_context().span_id

        # test that span and trace ids are valid
        assert isinstance(trace_id, int)
        assert isinstance(span_id, int)

    def test_ASpan_get_span_no_span_name_no_attrs(
            self,
            AnacondaTracer: AnacondaTrace,
            ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        Performs the same checks as the previous test, but in the case that span_name and attributes are both equal to None
        """
        ASpan = ASpanFactory(AnacondaTracer, span_name=None, attributes=None)

        # test that ASpan was created
        assert isinstance(ASpan._span, Span)

        trace_id = ASpan._span.get_span_context().trace_id
        span_id = ASpan._span.get_span_context().span_id

        # test that span and trace ids are valid
        assert isinstance(trace_id, int)
        assert isinstance(span_id, int)

    @patch('opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter')
    def test_setup_tracing_http(
        self,
        mock_exporter_http: MagicMock,
        AnacondaTracer: AnacondaTrace
    ):
        """
        - Checks that the tracer object returned by the method is of type Tracer (otel sdk object)
        - Checks that the OTLPSpanExporter from http library a called once
        """

        config = Config(default_endpoint="http://localhost")
        tracer = AnacondaTracer._setup_tracing(config)
        mock_exporter_http.assert_called_once()

        # Assert tracer is a valid Tracer object
        assert isinstance(tracer, Tracer)

    @patch('opentelemetry.exporter.otlp.proto.grpc.trace_exporter.OTLPSpanExporter')
    def test_setup_tracing_grpc(
        self,
        mock_exporter_grpc: MagicMock,
        AnacondaTracer: AnacondaTrace
    ):
        """
        - Checks that the tracer object returned by the method is of type Tracer (otel sdk object)
        - Checks that the OTLPSpanExporter from grpc library was called once
        """
        AnacondaTracer._request_protocol = 'grpc'
        config = Config(default_endpoint="grpc://localhost")
        tracer = AnacondaTracer._setup_tracing(config)
        mock_exporter_grpc.assert_called_once()

        # Assert tracer is a valid Tracer object
        assert isinstance(tracer, Tracer)

    def test_ASpan_add_event_valid_name(
        self,
        AnacondaTracer: AnacondaTrace,
        ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        - Checks that the `get_span` method still returns a valid Span object
        - Checks that the ASpan.span object's most recent event name matches the expected event name
        """
        span_name = "test-span"
        ASpan = ASpanFactory(AnacondaTracer, span_name=span_name, attributes={"test": "1"})

        event_str = "hello"
        ASpan.add_event(event_str)

        # there is a span event on init indicating start so we test most recent
        assert isinstance(ASpan._span, Span)

    def test_ASpan_add_event_no_name(
        self,
        AnacondaTracer: AnacondaTrace,
        ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        - Checks that the get_span method still returns a valid Span object
        - Checks that the ASpan.span object's most recent event name matches the expected event name when None is passed
        """
        span_name = "test-span"
        ASpan = ASpanFactory(AnacondaTracer, span_name=span_name, attributes={"test": "1"})

        event_str = None
        ASpan.add_event(event_str)

        # assert that we still have an instance of span
        assert isinstance(ASpan._span, Span)

    def test_ASpan_add_exception_valid_exception(
        self,
        AnacondaTracer: AnacondaTrace,
        ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        - Checks again that `get_span` returns a valid Span object
        - Checks that the most recent event name for the ASpan.span object matches the expected event name after an exception is passed
        - Checks that the "error.message" attribute for the ASpan.span object matches the expected err_msg
        """
        span_name = "test-span"
        ASpan = ASpanFactory(AnacondaTracer, span_name=span_name, attributes={"test": "1"})
        err_msg = "This is a test exception"
        exception = Exception(err_msg)
        ASpan.add_exception(exception)

        # there is a span event on init indicating start so we test most recent
        assert isinstance(ASpan._span, Span)

    def test_ASpan_add_exception_none_exception(
        self,
        AnacondaTracer: AnacondaTrace,
        ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        - Checks that the get_span method still returns a valid Span object
        - Checks that the "error.message" attribute for the ASpan.span object matches the expected generic error message for when None is passed as the exception
        """
        span_name = "test-span"
        ASpan = ASpanFactory(AnacondaTracer, span_name=span_name, attributes={"test": "1"})
        exception = None
        ASpan.add_exception(exception)

        # generic_err_msg is hard coded as the fallback case in _AnacondaTrace.ASpan
        generic_err_msg = "Generic exception because the exception passed was None."

        assert isinstance(ASpan._span, Span)

    def test_ASpan_set_error_status(
        self,
        AnacondaTracer: AnacondaTrace,
        ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        - Checks that ASpan.status == StatusCode.ERROR after the method is called
        """
        span_name = "test-span"
        ASpan = ASpanFactory(AnacondaTracer, span_name=span_name, attributes={"test": "1"})
        ASpan.set_error_status()
        # The Span object is opaque, cannot check if it was set.

    def test_ASpan_add_attributes(
        self,
        AnacondaTracer: AnacondaTrace,
        ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        - Checks add_attributes method adds attributes to the ASpan.span object.
        """
        span_name = "test-span"
        ASpan: AnacondaTrace.ASpan = ASpanFactory(AnacondaTracer, span_name=span_name, attributes={"test": "1"})
        ASpan._noop = False
        ASpan._span = MagicMock()
        assert len(ASpan._attributes) == 1  # initial attributes
        ASpan.add_attributes({"key1": "value1", "key2": "value2"})
        golden_attributes = {
            "key1": "value1",
            "key2": "value2",
            "test": "1"  # existing attributes should not be overwritten
        }
        assert len(ASpan._attributes) == len(golden_attributes)
        for key in golden_attributes.keys():
            assert ASpan._attributes[key] == golden_attributes[key]

        with pytest.raises(TypeError):
            # Test that TypeError is raised when non-dict is passed
            ASpan.add_attributes("not a dict")

        ASpan._noop = True  # Simulate noop span
        ASpan.add_attributes({"key3": "value3"})

        assert len(ASpan._attributes) == len(golden_attributes)
        for key in golden_attributes.keys():
            assert ASpan._attributes[key] == golden_attributes[key]

        ASpan._noop = False  # Simulate noop span
        ASpan.set_error_status()

        ASpan._close()

    def test_ASpan_close_event(
        self,
        AnacondaTracer: AnacondaTrace,
        ASpanFactory: Callable[[AnacondaTrace, str, Dict[str, str]], object]
    ):
        """
        - Checks that the most recent span event after this method is called is one with end in the name
        """
        span_name = "test-span"
        ASpan: AnacondaTrace.ASpan = ASpanFactory(AnacondaTracer, span_name=span_name, attributes={"test": "1"})
        ASpan._noop = True
        assert isinstance(ASpan._span, Span)
        ASpan._close()

class TestAnacondaMetrics:
    instance: AnacondaMetrics = None

    @pytest.fixture(scope="class")
    def AnacondaMetric(self) -> AnacondaMetrics:
        if TestAnacondaMetrics.instance is None:
            config_values = read_config()
            config_dict, attributes_dict = config_values['configs'], config_values['attributes']
            config_dict['entropy'] = "timestamp"  # this value is required and normally initialized by initialize_telemetry()
            config = Config(config_dict=config_dict)
            attributes = Attributes("test-service", "1.0.0")
            attributes.set_attributes(**attributes_dict)
            # initialize class for testing
            with patch('opentelemetry.metrics.set_meter_provider'):
                TestAnacondaMetrics.instance = AnacondaMetrics(config, attributes)
                TestAnacondaMetrics.instance.use_console_exporters = False
                TestAnacondaMetrics.instance.logger = MagicMock()

        return TestAnacondaMetrics.instance

    @patch('opentelemetry.exporter.otlp.proto.http.metric_exporter.OTLPMetricExporter')
    def test_setup_metrics_http(self, mock_exporter_http: MagicMock, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that metrics object returned by the method is of type Meter (otel sdk object)
        - Checks that http library is called for exporter
        """
        mock_exporter_http.__name__ = 'OTLPMetricExporter'
        config = Config(default_endpoint="http://localhost")
        metrics = AnacondaMetric._setup_metrics(config)
        mock_exporter_http.assert_called_once()

        # ensure returned object is of type Meter
        assert isinstance(metrics, Meter)

    @patch('opentelemetry.exporter.otlp.proto.grpc.metric_exporter.OTLPMetricExporter')
    def test_setup_metrics_grpc(self, mock_exporter_grpc: MagicMock, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that metrics object returned by the method is of type Meter (otel sdk object)
        - Checks that grpc library is called for exporter
        """
        config = Config(default_endpoint="grpc://localhost")
        metrics = AnacondaMetric._setup_metrics(config)
        mock_exporter_grpc.assert_called_once()

        # ensure returned object is of type Meter
        assert isinstance(metrics, Meter)

    def test_catch_space_in_metric_name(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that the logger logs a warning matching the invalid regex string when an invalid metric name is passed
        - Checks that meter objects is an empty dict, meaning nothing has been initialized
        """
        AnacondaMetric.logger = MagicMock()
        name = "hello world"
        AnacondaMetric._get_or_create_metric(name)

        AnacondaMetric.logger.warning.assert_called_once_with(
            f"Metric {name} does not match valid regex: r\"^[A-Za-z][A-Za-z_0-9]+$\""
        )
        assert AnacondaMetric.type_list["simple_up_down_counter"] == {}

    def test_setup_manual_metrics_invalid_type(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that the logger logs a warning matching the invalid type string when an invalid metric type is passed
        - Checks that meter objects is an empty dict, meaning nothing has been initialized
        """
        AnacondaMetric.logger = MagicMock()
        AnacondaMetric.create_dispatcher = {
            "simple_counter": MagicMock()
        }
        name = "bad_type_metric"
        type = "not_real_type"

        with pytest.raises(RuntimeError):
            AnacondaMetric._get_or_create_metric(name, metric_type=type)

    def test_setup_manual_metrics_success(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that the simple_counter dispatcher was called exactly once with arguments matching name, unit, and desc
        - Checks that meter objects contains a key of the newly added metric name
        """
        # this function must go after all the empty dict assertions
        # scope of the AnacondaMetric is the class so new manual metrics persist

        create_mock = MagicMock()
        AnacondaMetric.create_dispatcher = {
            'simple_counter': create_mock
        }

        name = "test_counter"
        desc = "A test counter"
        unit = "1"

        AnacondaMetric._get_or_create_metric(name, metric_type='simple_counter', units=unit, description=desc)

        create_mock.assert_called_once_with(
            name, unit=unit, description=desc
        )
        assert name in AnacondaMetric.type_list['simple_counter']

    def test_record_histogram_success(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that method returns True given assembled inputs
        - Checks that _Histogram was called exactly once with expected arguments
        """
        mock_metric = MagicMock()

        # Inject a fake metric into the instance
        AnacondaMetric.type_list["histogram"]['my_histogram'] = mock_metric

        value = 42.0

        result = AnacondaMetric.record_histogram("my_histogram", value, {"tag": "test"})

        assert result is True
        mock_metric.record.assert_called_once_with(value, {"tag": "test"})

    def test_increment_counter_success_counter(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that method returns False given correctly assembled inputs
        - Checks that _Counter was called exactly once with expected arguments
        """
        mock_metric = MagicMock()
        mock_metric.__class__.__name__ = "_Counter"

        AnacondaMetric.type_list["simple_counter"]["my_counter"] = mock_metric

        unit = 3
        result = AnacondaMetric.increment_counter("my_counter", by=unit, attributes={"tag": "test"})

        assert result is True
        mock_metric.add.assert_called_once_with(unit, {"tag": "test"})

    def test_increment_counter_success_updowncounter(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that method returns True given assembled inputs
        - Checks that _UpDownCounter was called exactly once with expected arguments
        """
        mock_metric = MagicMock()
        mock_metric.__class__.__name__ = "_UpDownCounter"

        AnacondaMetric.type_list["simple_up_down_counter"]["my_updown"] = mock_metric

        result = AnacondaMetric.increment_counter("my_updown", by=-2, attributes={"reason": "decrement"})

        assert result is True
        mock_metric.add.assert_called_once_with(2, {"reason": "decrement"})

    def test_increment_counter_default_by_and_attributes(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that method returns True after correctly falling back to default inputs
        - Checks that _Counter was called exactly once with expected default arguments
        """
        mock_metric = MagicMock()
        mock_metric.__class__.__name__ = "_Counter"

        AnacondaMetric.type_list["simple_counter"]["default_metric"] = mock_metric

        result = AnacondaMetric.increment_counter("default_metric")

        assert result is True
        mock_metric.add.assert_called_once_with(1, {})  # Default by=1, attributes={}

    def test_decrement_counter_success(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that method returns True given assembled inputs
        - Checks that _UpDownCounter was called exactly once with expected arguments
        """
        mock_metric = MagicMock()
        mock_metric.__class__.__name__ = "_UpDownCounter"

        AnacondaMetric.type_list["simple_up_down_counter"]["my_updown"] = mock_metric

        result = AnacondaMetric.decrement_counter("my_updown", by=3, attributes={"reason": "adjustment"})

        assert result is True
        mock_metric.add.assert_called_once_with(-3, {"reason": "adjustment"})

    def test_decrement_counter_default_arguments(self, AnacondaMetric: AnacondaMetrics):
        """
        - Checks that method returns True after correctly falling back to default inputs
        - Checks that _UpDownCounter was called exactly once with expected default arguments
        """
        mock_metric = MagicMock()
        mock_metric.__class__.__name__ = "_UpDownCounter"

        AnacondaMetric.type_list["simple_up_down_counter"]["default_case"] = mock_metric

        result = AnacondaMetric.decrement_counter("default_case")

        assert result is True
        mock_metric.add.assert_called_once_with(-1, {})  # Default by=1, attributes={}

    def test_preferred_temporality(self):
        """
        - Checks that the temporaity is cumulative when set by caller.
        """
        cfg = Config(default_endpoint="http://localhost/v1/metrics")
        cfg.set_use_cumulative_metrics(True).set_console_exporter(True)
        attr = Attributes("test-service", "1.0.0")
        with patch('opentelemetry.metrics.set_meter_provider'):
            metrics = AnacondaMetrics(cfg, attr)
            assert metrics._cumulative_temporality == metrics._get_temporality()

class MockHistogram(Histogram):
    def __init__(self):
        self.counter = 0
        self.last_value = None
        self.last_attr = {}

    def record(self, amount: Union[int, float], attr: AttrDict = None, context: Context = None):
        self.counter += 1
        self.last_value = amount
        self.last_attr = attr
