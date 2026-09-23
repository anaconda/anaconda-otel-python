# Best Practices for Product Telmetry with OpenTelemetry

## Deciding on a Signal Type (Traces vs Metrics vs Logs)
There are three main signal types in OpenTelemetry (and general observability) and each one has tradeoffs that suit them to specific use cases. In OpenTelemetry, each signal type has a specific structure.
- Metrics contain groups of counter or measurement records, and these records contain numeric properties and metric scopes
- Traces are groupings of individual events (spans) that share parent/child relationships or context
- Logs contain a text body

### Logs
For product telemetry we typically want to be using logs. Most often the primary interests of product telemetry are an event that occurred and the context behind it. The attributes actually are just as important as the simple presence of the event. Attibutes convey event context, like which user, which org, or which package. This case matches product events better with logs than with metrics and traces, and are superior in regards to payload size and shape compared to the other signals as well. Typically ending up in Snowflake, product telemetry doesn't benefit as handsomely from the tsdb payload features metrics have. 

When many developers think of logs, they think of application/developer logs. And if you desire those logs to be part of your telemetry then the logger handler should be configured. But it's more likely the telemetry corresponds to event data. If this is the case using `send_event()` can register telemetry events this way.

Beyond size and shape, another reason to use logs rather than metrics is cardinality. Product telemetry typically carries one or more high cardinality attributes (user id, username, etc.) which OpenTelemetry metrics are not optimized for. 


#### Visual Example of a log payload
```
{
    "scopeLogs": [
    {
        "scope": {
        "name": "my_logger"
        },
        "logRecords": [
            {
                "timeUnixNano": "1767993488934098944",
                "observedTimeUnixNano": "1767993488934126000",
                "body": {
                    "stringValue": "Hello"
                },
                "attributes": [
                    {
                        "key": "log.event.name",
                        "value": {
                        "stringValue": "test.event"
                        }
                    }
                ],
            }
        ]
    }
    ]
}
```

### Simple Event Logs
If your product is using logs to capture events rather than to capture developer logs, the `EventLogger` class invoked by the `send_event` function in our code is a more efficient method of transporting events. These calls produce the lightest payloads. If you are not interested in capturing the line numbers, log levels, etc. that come with standard developer logs, this would be the way to go.

#### Visual example of Event Log payload
```
{
    "scope_logs": [
    {
        "scope": {
        "name": "aau_test_event_logger"
        },
        "log_records": [
        {
            "body": {
            "string_value": "Hello"
            },
            "attributes": [
            {
                "key": "log.event.name",
                "value": {
                "string_value": "test_event"
                }
            }
            ],
            "observed_time_unix_nano": "1777304261742595000"
        }
        ]
    }
    ]
}
```

### Metrics
If an event or piece of code you want telemetry for can be presented numerically, then the use case is best for metrics. Several examples include:
- User login event (increment by 1)
- Query event in AI Catalog (increment by 1)
- Response time in milliseconds (add to distribution)
- RAM utilized by a machine in megabytes (gauge the signal)

It is recommended to use metrics when the cardinality of events is lower than most product telemetry use cases. Something like a user id alone is not ideal to be added to metrics.

#### Visual Example of a Metric
```
{
    "scopeMetrics": [
    {
        "scope": {
        "name": "test_service",
        "version": "dev-build"
        },
        "metrics": [
        {
            "name": "test",
            "description": "No description.",
            "unit": "#",
            "sum": {
            "dataPoints": [
                {
                "attributes": [
                    {
                    "key": "user.id",
                    "value": {
                        "stringValue": "test123"
                    }
                    }
                ],
                "startTimeUnixNano": "1767886298183762000",
                "timeUnixNano": "1767886298183888000",
                "asInt": "1"
                }
            ],
            "aggregationTemporality": 2
            }
        }
        ]
    }
    ]
}
```

### Traces
When the context of a group of events matters, such as a request path or the route of multiple interconnected events, traces are the signal type to use. The most common use case is request tracing across distributed systems, with user journeys being another possibility. In the case of tracing, the context is the important part. If the events in code do not matter in relation to each other then they should never be a trace.

Traces are made up of spans. Spans are the individual events - such as a request to Service A - with traces being the container grouping spans together. This grouping happens with instrumentation via the sharing of context, which is created on the initial call and typically passed via request headers. The context could also be passed via function parameters for a use case like tracking user journeys within a single application.

Spans have parent/child relationships. The context contains the most recent span, so when a new span is created if there is context to be extracted then the new span can refer to the previous span as its parent. Consider the following example:
- Request from client to Service A
- The request to Service A results in a call to Service B, where the chain of events ends

Trace telemetry for this event would be a single trace. It would contain the parent span representing the call to Service A from the client, and the parent span's child span which represents the call from Service A to Service B. If service B was also instrumented then there would be a third span. This one would just be the child of the span representing the call from Service A to Service B, and not have any child spans itself because there are no more requests generated by this API route.

#### Visual example of a trace payload:
In this example Service A calls service B which calls service C, and the chain ends there. Note the empty `parent_id` for the root parent span, and the matching `parent_id` of each subsequent span to its parent's `span_id`.
```
{
    "name": "serviceC.process",
    "context": {
        "trace_id": "0x16beb6ad8f552cd02b12810da6e7ba40",
        "span_id": "0x3f9017e98c9dd191",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": "0x1d8619fc37fb1436",
    "start_time": "2026-01-08T20:27:42.584024Z",
    "end_time": "2026-01-08T20:27:42.584052Z",   
}
{
    "name": "serviceB.process",
    "context": {
        "trace_id": "0x16beb6ad8f552cd02b12810da6e7ba40",
        "span_id": "0x1d8619fc37fb1436",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": "0x5df37dadbdc8180b",
    "start_time": "2026-01-08T20:27:42.582757Z",
    "end_time": "2026-01-08T20:27:42.585265Z",
}
{
    "name": "serviceA.process",
    "context": {
        "trace_id": "0x16beb6ad8f552cd02b12810da6e7ba40",
        "span_id": "0x5df37dadbdc8180b",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2026-01-08T20:27:42.581063Z",
    "end_time": "2026-01-08T20:27:42.585825Z",
}
```