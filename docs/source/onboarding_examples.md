# Examples of anaconda-opentelemetry usage
These examples serve as an onboarding guide and as further explanations to main documentation.

## Configuration
### Creating Configuration
```python
try:
    config = Configuration(default_endpoint='example.com:4317', default_auth_token=token)
    config.set_metrics_export_interval_ms(10000).set_logging_level('warn')
except:
    logging.warning("Telemetry `Configuration` failed to be created")
```
### Specific Endpoint for Signal
```python
config.set_metrics_endpoint(
    endpoint='http://localhost:4318',
    auth_token=token,
    cert_ca_file='./ca_cert.cer'
)
```

### Optional Session Entropy
```python
entropy_value = time.time()  # current unix time - simple form of entropy
try:
    config = Configuration(default_endpoint='example.com:4317').set_tracing_session_entropy(entropy_value)
except:
    # code here
```

## ResourceAttributes
```python
service_name, service_version = "service-a", "v1"
try:
    attributes = ResourceAttributes(service_name, service_version)
    attributes.set_attributes(environment="production", platform="aws")
except:
    logging.warning(f"Telemetry `ResourceAttributes` failed to be created")
```

### Adding more attributes
```python
try:
    attributes = ResourceAttributes(service_name, service_version)
    attributes.set_attributes(random_attribute_key="test1", random_attribute_key2="test2")
except:
    logging.warning(f"Telemetry `ResourceAttributes` failed to be created")
```

## Initializing Telemetry
```python
from anaconda_opentelemetry import *

attributes = ResourceAttributes("service-a", "v1")
try:
  initialize_telemetry(
      config=config,
      attributes=attributes
  )
except:
  logging.warning(f"Telemetry failed to be initialized.")
```

### Optional Signal Streams
Try except omitted in this example:
```python
initialize_telemetry(
    config=config,
    attributes=attributes,
    signal_types=["tracing", "metrics"]
)
```

## Recording Telemetry

### Logs
```python
log = logging.getLogger("your_logger_name_here")
try:
    log.addHandler(get_telemetry_logger_handler())
except:
  log.warning(f"OpenTelemetry logger failed to be initialized.")
```

### Metrics
These functions do not need additional error handling. They will all catch exceptions.

#### Histogram

```python
from anaconda_opentelemetry.signals import *

record_histogram("request_duration_ms", value=123.4, attributes={"route": "/home"})
```

#### Counter (Increment)

```python
from anaconda_opentelemetry.signals import *

increment_counter("active_sessions", by=1, attributes={"region": "us-east"})
```

#### Counter (Decrement)
Restricted to type `simple_up_down_counter`.

```python
from anaconda_opentelemetry.signals import *

decrement_counter("active_sessions", by=1, attributes={"region": "us-east"})
```

### Traces
This function does not need additional error handling. It will all catch exceptions.

```python
from anaconda_opentelemetry.signals import *

with get_trace("process_data", attributes={"job_id": "abc-123"}):
    # Your business logic here
    process_data()
```

## Schema
```python
attrs = ResourceAttributes(
  "test_service",  # service_name requires a user-supplied value, not a keyword arg
  "v1",  # service_version requires a user-supplied value, not a keyword arg
  os_type="Darwin",
  os_version="24.2.0",
  python_version="3.13.2",
  hostname="Users-MBP"
)
```

### Dynamic Resource Attributes in the Schema
Passing kwargs to the ResourceAttributes set_attributes method
```python
attrs = ResourceAttributes("test-service", "1").set_attributes(foo="test")
```
Or passing a dictionary
```python
my_attributes = {
  "test1": "one",
  "test2": "two"
}
attrs = ResourceAttributes("test-service", "1").set_attributes(**my_attributes)
```

# Testing and Visualizing Telemetry Locally
To test the telemetry package and view exports locally, the following code can be used. The console exporter exports telemetry payloads to standard output:
```python
from anaconda_opentelemetry.signals import initialize_telemetry, increment_counter
from anaconda_opentelemetry.attributes import ResourceAttributes
from anaconda_opentelemetry.config import Configuration

cfg = Configuration(default_endpoint='http://localhost:4318').set_console_exporter(use_console=True)
att = ResourceAttributes("test_service", "dev-build", environment="test")
initialize_telemetry(config=cfg, attributes=att, signal_types=['metrics'])

increment_counter("test", by=1)
```