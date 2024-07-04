## Span profiles support for OpenTelemetry in Python

This package enables applications that already rely on [OpenTelemetry](https://opentelemetry.io/docs/instrumentation/python/getting-started/) for distributed tracing and Pyroscope for continuous profiling to link the tracing and profiling data together.

See https://grafana.com/docs/pyroscope/latest/configure-client/trace-span-profiles/ for more information.

### Prerequisites
- Your Python application is instrumented with [Pyroscope's profiler](https://grafana.com/docs/pyroscope/latest/configure-client/language-sdks/python/)
- Your Python application is instrumented with [OpenTelemetry](https://opentelemetry.io/docs/instrumentation/python/getting-started/)

### Integration

Add the following package to your project:

```shell
pip install pyroscope-otel
```

Register the `PyroscopeSpanProcessor` in your OpenTelemetry integration:

```python

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

from pyroscope-otel import PyroscopeSpanProcessor

provider = TracerProvider()
provider.add_span_processor(PyroscopeSpanProcessor())

trace.set_tracer_provider(provider)

```
