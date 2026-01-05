# Best Practices for Product Telmetry with OpenTelemetry

## Deciding on a Signal Type (Traces vs Metrics vs Logs)
There are three main signal types in OpenTelemetry (and general observability) and each one has tradeoffs that suit them to specific use cases. In OpenTelemetry, each signal type has a specific structure.
- Metrics contain groups of recorded numbers and measurements, and these records contain numeric properties and metric scopes
- Traces contain elements that are groupings of events that share parent/child relationships or context, each event contains event attributes
- Logs contain a text body, each body contains optional attributes

### Metrics
Metrics are ideal to use when the telemetry you want to collect can be made numerical. If an event or piece of code you want telemetry for can be represented by a number, then the use case is best for metrics. Several examples include:
- User login event (increment by 1)
- Query event in AI Catalog (increment by 1)
- Response time in milliseconds (add to distribution)
- RAM utilized by a machine in megabytes (gauge the signal)

This does not necessarily mean that the primary interest in the telemetry is the number of user login events. You could be collecting this telemetry event because you're more interested in the characteristics of who logged in. Even still, the metric signal type is the best fit. OpenTelemetry packages metrics of the same name together in groups containing each individual event. It uses a set structure and fixed properties for all metrics to form consist payload contents. This makes metrics easier for backends to collate and query, and you'll be able to see specific metric events containing specific sets of labels. 

### Traces
