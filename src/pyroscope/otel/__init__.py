import typing

from opentelemetry.sdk.trace import (
    Span,
    ReadableSpan,
    SpanProcessor,
)
from opentelemetry.context import Context

import pyroscope

PROFILE_ID_SPAN_ATTRIBUTE_KEY = 'pyroscope.profile.id'
PROFILE_ID_PYROSCOPE_TAG_KEY = 'span_id'
SPAN_NAME_PYROSCOPE_TAG_KEY = 'span_name'
TRACE_ID_PYROSCOPE_TAG_KEY = 'trace_id'

def _is_root_span(span: Span):
    return span.parent is None or span.parent.is_remote

def _get_span_id(span: Span):
    return format(span.context.span_id, "016x")

def _get_trace_id(span: Span):
    return format(span.context.trace_id, "032x")

# A span processor that sets a common identifier in spans and profiling samples, so that they can be linked together.
class PyroscopeSpanProcessor(SpanProcessor):

    def __init__(self, trace_id_enabled: bool = True):
        self._trace_id_enabled = trace_id_enabled

    def on_start(
        self, span: Span, parent_context: typing.Optional[Context] = None
    ) -> None:
        if _is_root_span(span):
            span.set_attribute(PROFILE_ID_SPAN_ATTRIBUTE_KEY, _get_span_id(span))
            pyroscope.add_thread_tag(PROFILE_ID_PYROSCOPE_TAG_KEY, _get_span_id(span))
            pyroscope.add_thread_tag(SPAN_NAME_PYROSCOPE_TAG_KEY, span.name)
            if self._trace_id_enabled:
                pyroscope.add_thread_tag(TRACE_ID_PYROSCOPE_TAG_KEY, _get_trace_id(span))

    def on_end(self, span: ReadableSpan) -> None:
        if _is_root_span(span):
            pyroscope.remove_thread_tag(PROFILE_ID_PYROSCOPE_TAG_KEY, _get_span_id(span))
            pyroscope.remove_thread_tag(SPAN_NAME_PYROSCOPE_TAG_KEY, span.name)
            if self._trace_id_enabled:
                pyroscope.remove_thread_tag(TRACE_ID_PYROSCOPE_TAG_KEY, _get_trace_id(span))

    def shutdown(self) -> None:
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True
