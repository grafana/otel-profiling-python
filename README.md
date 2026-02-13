# Span Profiles Support for OpenTelemetry in Python

This package links OpenTelemetry tracing data with Pyroscope continuous profiling data, enabling you to correlate traces with performance profiles.

Reference: https://grafana.com/docs/pyroscope/latest/configure-client/trace-span-profiles/

## Prerequisites

- Your Python application is instrumented with [Pyroscope profiler](https://grafana.com/docs/pyroscope/latest/configure-client/language-sdks/python/)
- Your Python application is instrumented with [OpenTelemetry](https://opentelemetry.io/docs/instrumentation/python/getting-started/)

## Installation
```shell
pip install pyroscope-otel
```

## Pyroscope Configuration (Required)

Pyroscope must be configured before creating any spans. This is mandatory for all setups:
```python
from pyroscope import configure as pyroscope_configure

# Local setup (default)
pyroscope_configure(
    app_name="my-app",
    server_address="http://localhost:4040",
    sample_rate=100,
)

# Grafana Cloud setup (uncomment and update with your credentials)
# pyroscope_configure(
#     app_name="my-app",
#     server_address="https://pyroscope-blocks-prod-us-central-1.grafana-cloud.com/prom/push",
#     auth_token="<your-grafana-cloud-token>",
#     basic_auth_username="<your-username>",  # Optional: username for basic auth (Grafana Cloud)
#     basic_auth_password="<your-password>",  # Optional: password for basic auth (Grafana Cloud)
#     sample_rate=100,
# )
```

## How It Works & Span Attributes

The `PyroscopeSpanProcessor` automatically attaches the profile identifier (`pyroscope.profile.id`) as an attribute to the **root span** of each trace. This creates a direct link between traces and their corresponding performance profiles in Grafana Tempo, allowing you to navigate from any trace to the exact performance profile data for that transaction.

## Manual Instrumentation

Configure OpenTelemetry explicitly (after Pyroscope is already configured):
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from pyroscope.otel import PyroscopeSpanProcessor

# Configure OpenTelemetry
provider = TracerProvider()
provider.add_span_processor(PyroscopeSpanProcessor())

# TODO: Add your trace exporter configuration here
# (e.g., Grafana Tempo OTLP exporter, etc.)
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# provider.add_span_processor(BatchSpanProcessor(your_exporter))

trace.set_tracer_provider(provider)

# Use tracing in your application
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my_operation"):
    # Your code here
    pass
```

## Automatic Instrumentation

When using auto-instrumentation (e.g., `opentelemetry-distro`), you must still register `PyroscopeSpanProcessor` manually (after Pyroscope is already configured):
```python
from opentelemetry import trace
from pyroscope.otel import PyroscopeSpanProcessor

# After auto-instrumentation is initialized
provider = trace.get_tracer_provider()
provider.add_span_processor(PyroscopeSpanProcessor())
```

> **Note:** Auto-instrumentation only handles OpenTelemetry setup. Pyroscope configuration is still required.

## Grafana Cloud OpenTelemetry Exporter (Optional)
```python
# OpenTelemetry exporter for Grafana Cloud / Grafana Tempo
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
#
# otlp_exporter = OTLPSpanExporter(
#     endpoint="<your-tempo-instance>.grafana.net:443",
#     headers=(("Authorization", "Bearer <your-grafana-cloud-token>"),),
# )
# provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
```

## Integration Checklist

- ✅ Pyroscope configured with `pyroscope_configure()`
- ✅ OpenTelemetry `TracerProvider` created
- ✅ `PyroscopeSpanProcessor` registered with `add_span_processor()`
- ✅ Trace exporter configured (Grafana Tempo, etc.)
- ✅ Application instrumented with OpenTelemetry
- ✅ Verify `pyroscope.profile.id` appears in span attributes in Grafana Tempo

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pyroscope.profile.id` not in spans | Ensure `PyroscopeSpanProcessor` was registered with `add_span_processor()` |
| Profiles not appearing in Pyroscope | Verify `pyroscope_configure()` is called before creating spans |
| Traces not exporting | Check trace exporter configuration and credentials |
| Auto-instrumentation not working | Manually add `PyroscopeSpanProcessor()` after initializing the provider |

## References

- [Pyroscope Documentation](https://grafana.com/docs/pyroscope/latest/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Trace-Profile Integration](https://grafana.com/docs/pyroscope/latest/configure-client/trace-span-profiles/)
