# Examples of anaconda-opentelemetry usage

## Configuration
### Creating Configuration
```python
config = Configuration(default_endpoint='example.com:4317', default_auth_token=token)
config.set_metrics_export_interval_ms(10000).set_logging_level('warn')
```
### Specific Endpoint
```python
config.set_metrics_endpoint(
    endpoint='http://localhost:4318',
    auth_token=token,
    cert_ca_file='./ca_cert.cer'
)
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
  # Handle error in the application.
```