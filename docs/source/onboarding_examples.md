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