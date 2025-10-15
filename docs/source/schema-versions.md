# Schema Versions for `anaconda-opentelemetry` Payloads
This schema refers to the resource.attributes portion of the OpenTelemetry payload. The rest of the payload's structure is not managed by the anaconda-opentelemetry package.

## [v0.2.0] (07/18/25) - Current Schema
```
{
  "telemetry.sdk.language": "python",  # added by Otel
  "telemetry.sdk.name": "opentelemetry",  # added by Otel
  "telemetry.sdk.version": "1.33.1",  # added by Otel   
  "service.name": "platform-service",
  "service.version": "x.x.x",
  "os.type": "Darwin",
  "os.version": "x.x.x",
  "python.version": "3.13.2",
  "hostname": "Users-MBP",
  "client.sdk.version": "x.x.x",
  "schema.version": "x.x.x",
  “platform”: “Such as cloud provider”,
  “environment”: “”,  # an enum. Must be one of {“”, “test”, “development”, “staging”, “production”}
  "user.id": "12345",  # or similar
  "session.id": "ac8fk…",  # hash set by anaconda-opentelemetry
  "parameters": {...}  # optional dynamic values for flexibility - json object of key value pairs
}
```

## [v0.1.0] (06/18/25)
```
{
  "telemetry.sdk.language": "python",  # added by Otel
  "telemetry.sdk.name": "opentelemetry",  # added by Otel
  "telemetry.sdk.version": "1.33.1",  # added by Otel   
  "service.name": "platform-service",  # required by Otel to use dot notation
  "service.version": "x.x.x",  # required by Otel to use dot notation
  "os_type": "Darwin",
  "os_version": "x.x.x",
  "python_version": "3.13.2",
  "hostname": "Users-MBP",
  "client_sdk_version": "x.x.x",
  "schema_version": "x.x.x",
  “platform”: “Such as cloud provider”,
  “environment”: “”,  # an enum. Must be one of {“”, “test”, “development”, “staging”, “production”}
  "user_id": "12345",  # or similar
  "session_id": "ac8fk…",  # hash set by anaconda-opentelemetry
  "parameters": {...}  # optional dynamic values for flexibility - json object of key value pairs
}
```

## Example Full OpenTelemetry Payload  - [Schema v0.2.0]
```
{
  "resource_metrics": [
    {
      "resource": {
        "attributes": {
          "telemetry.sdk.language": "python",
          "telemetry.sdk.name": "opentelemetry",
          "telemetry.sdk.version": "1.33.1",
          "service.name": "example-metrics-app",
          "service.version": "1.0.0",
          "os.type": "Darwin",
          "os.version": "24.4.0",
          "python.version": "3.13.2",
          "hostname": "Users-MBP",
          “environment”: “production”,
          "client.sdk.version": "1.0.0",
          "schema.version": "1.0.0",
          "session.id": "ac8fk…"
          "parameters": "{}"
        },
        "schema_url": ""
      },
      "scope_metrics": [
        {
          "scope": {
            "name": "example-meter",
            "version": "",
            "schema_url": "",
            "attributes": null
          },
          "metrics": [
            {
              "name": "request_duration",
              "description": "Request duration in milliseconds",
              "unit": "ms",
              "data": {
                "data_points": [
                  {
                    "attributes": {
                      "endpoint": "/api/users",
                      "method": "GET"
                    },
                    "start_time_unix_nano": 1750113562322143000,
                    "time_unix_nano": 1750113562322212000,
                    "count": 1,
                    "sum": 126.9028115948253,
                    "bucket_counts": [
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0
                    ],
                    "explicit_bounds": [
                      0.0,
                      5.0,
                      10.0,
                      25.0,
                      50.0,
                      75.0,
                      100.0,
                      250.0,
                      500.0,
                      750.0,
                      1000.0,
                      2500.0,
                      5000.0,
                      7500.0,
                      10000.0
                    ],
                    "min": 126.9028115948253,
                    "max": 126.9028115948253,
                    "exemplars": []
                  }
                ],
                "aggregation_temporality": 2
              }
            }
          ],
          "schema_url": ""
        }
      ],
      "schema_url": ""
    }
  ]
}
```