# Schema Versions for `anaconda-opentelemetry` Payloads
This schema refers to the `resource.attributes` and `scope_metrics.metrics.data.data_points.attributes` (event specific) portion of the OpenTelemetry payload. The rest of the payload's structure is not managed by the anaconda-opentelemetry package.

## Current Schema
### [v0.3.0] (12/01/2025)
```
{
  "resourceMetrics|resourceLogs": [
    {
      "resource": {
        "attributes": {  # key value pairs within here are where data is added
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
          “platform”: “cloud provider”,
          “environment”: “”,  # an enum. Must be one of {“”, “test”, “development”, “staging”, “production”}
          "session.id": "ac8fk…",  # hash set by anaconda-opentelemetry
          "parameters": {...}  # optional dynamic values for flexibility - json object of key value pairs
        }
      }
      "scopeMetrics|scopeLogs": [
        ### Metrics -----------------------------------------------------------------
        {
          "metrics": [
            {
              "data": {
                "data_points": [
                  {
                    "attributes": [
                      {  # key value pairs within here are where data is added
                        "key": "user.id",  # moved from resource.attributes in v0.3.0
                        "value": {
                          "stringValue": "1234"
                        }
                      },
                      # this section also includes event specific attributes
                    ],
                  }
                ]
              }
            }
          ]
        }
        ### End Metrics -------------------------------------------------------------

        ### Logs --------------------------------------------------------------------
        {
          "logRecords": [
            {
              "attributes": [
                {  # key value pairs within here are where data is added
                  "key": "user.id",  # moved from resource.attributes in v0.3.0
                  "value": {
                    "stringValue": "1234"
                  }
                },
                # this section also includes event specific attributes
              ],
            }
          ]
        }
        ### End Logs ----------------------------------------------------------------
      ]
    }
  ]
}
```

## Definitions of schema properties
- Telemetry.sdk.language: set by OpenTelemetry’s SDK, denotes the language utilized
- Telemetry.sdk.name: set by OpenTelemetry’s SDK, name of SDK utilized
- Telemetry.sdk.version: set by OpenTelemetry’s SDK, version of SDK utilized
- Service.name (was Source): name of the client service sending telemetry
- Service.version: version of the client service sending telemetry
- Os.type: client operating system type
- Os.version: version of client operating system
- Python.version: python version used by client
- Hostname: hostname of client
- Client.sdk.version: version of the anaconda-opentelemetry package, set by package (readonly)
- Schema.version: version of the schema used in anaconda-opentelemetry package, set by package (readonly)
- Platform: The infrastructure on which the software is executed, which could include cloud providers (where is the user leveraging our products?)
- Environment: “” | test | development | staging | production
- Session.id: the setting of this is handled entirely by the anaconda-opentelemetry package, not the user. It is the result of hashing a session-unique string (readonly)
- Timestamp (automatically set): The UTC timestamp during which this event occurred
- Event: Custom event name defined per product
- Parameters: Optional values for the consumer to send in a dictionary format (this allows for flexibility of the schema). We decided on a nested pattern based on the established data platform patterns and processes.

## Historic Schemas
### [v0.2.0] (07/18/25) - (12/01/2025)
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

### [v0.1.0] (06/18/25)
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

## Example Full OpenTelemetry Metric Payload  - [Schema <= v0.2.0]
### All schemas newer than v0.2.0 show a full payload example
```
{
  "resourceMetrics": [
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