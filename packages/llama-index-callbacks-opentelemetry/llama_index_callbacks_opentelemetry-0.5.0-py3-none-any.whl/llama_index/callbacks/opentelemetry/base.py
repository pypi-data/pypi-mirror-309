from typing import Any, Dict, Optional
import inspect
import time

from opentelemetry import trace
from opentelemetry.trace import Span as OTelSpan, Status, StatusCode

from llama_index.core.instrumentation import get_dispatcher
from llama_index.core.instrumentation.events import BaseEvent
from llama_index.core.instrumentation.span.base import BaseSpan
from llama_index.core.instrumentation.span_handlers import BaseSpanHandler
from llama_index.core.instrumentation.event_handlers.base import BaseEventHandler


class OpenTelemetryEventHandler(BaseEventHandler):
    """Handler that converts LlamaIndex events to OpenTelemetry spans."""
    
    def __init__(self, tracer_name: str = "llama_index"):
        self.tracer = trace.get_tracer(tracer_name)
        
    @classmethod
    def class_name(cls) -> str:
        return "OpenTelemetryEventHandler"
        
    def handle(self, event: BaseEvent) -> None:
        """Convert LlamaIndex events to OpenTelemetry spans."""
        # Create a new span for this event
        with self.tracer.start_as_current_span(
            name=f"event.{event.class_name()}",
            kind=trace.SpanKind.INTERNAL
        ) as span:
            # Add event attributes to span
            span.set_attributes({
                "event.id": event.id_,
                "event.timestamp": event.timestamp,
                "event.type": event.class_name(),
            })
            
            # Add any additional event-specific attributes
            for field_name, field_value in event.model_dump().items():
                if field_name not in ["id_", "timestamp", "span_id"]:
                    # Sanitize/convert values as needed for OTel
                    if isinstance(field_value, (str, int, float, bool)):
                        span.set_attribute(f"event.{field_name}", field_value)
                    elif isinstance(field_value, (list, dict)):
                        # Convert complex types to string representation
                        span.set_attribute(f"event.{field_name}", str(field_value))


class OpenTelemetrySpanHandler(BaseSpanHandler):
    """Handler that converts LlamaIndex spans to OpenTelemetry spans."""
    
    def __init__(self, tracer_name: str = "llama_index"):
        self.tracer = trace.get_tracer(tracer_name)
        self._active_spans: Dict[str, OTelSpan] = {}
        
    @classmethod
    def class_name(cls) -> str:
        return "OpenTelemetrySpanHandler"
    
    def new_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        parent_span_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[BaseSpan]:
        """Create a new OpenTelemetry span."""
        # Get the current span context
        current_context = trace.get_current_span_context()

        # Determine the parent context
        parent_context = None
        if parent_span_id and parent_span_id in self._active_spans:
            parent_context = self._active_spans[parent_span_id].get_span_context()
        elif current_context.is_valid():
            parent_context = current_context

        # Start new span with the correct context
        context = trace.set_span_in_context(trace.INVALID_SPAN, context=parent_context)
        span = self.tracer.start_span(
            name=bound_args.signature.name,
            kind=trace.SpanKind.INTERNAL,
            context=context,
        )
        
        # Add basic attributes
        span.set_attributes({
            "span.id": id_,
            "span.start_time": time.time(),
        })
        
        # Add arguments as span attributes
        for arg_name, arg_value in bound_args.arguments.items():
            if isinstance(arg_value, (str, int, float, bool)):
                span.set_attribute(f"argument.{arg_name}", arg_value)
        
        # Add custom tags
        if tags:
            for tag_name, tag_value in tags.items():
                if isinstance(tag_value, (str, int, float, bool)):
                    span.set_attribute(f"tag.{tag_name}", tag_value)
        
        # Store active span
        self._active_spans[id_] = span
        
        return BaseSpan(id_=id_)
    
    def prepare_to_exit_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        result: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        """Handle normal span completion."""
        if span := self._active_spans.get(id_):
            # Add success status
            span.set_status(Status(StatusCode.OK))
            
            # Add result information if possible
            if isinstance(result, (str, int, float, bool)):
                span.set_attribute("result", str(result))
            
            # End span
            span.end()
            del self._active_spans[id_]
        
        return result
    
    def prepare_to_drop_span(
        self,
        id_: str,
        bound_args: inspect.BoundArguments,
        instance: Optional[Any] = None,
        err: Optional[BaseException] = None,
        **kwargs: Any,
    ) -> Any:
        """Handle span termination due to error."""
        if span := self._active_spans.get(id_):
            # Add error status and information
            span.set_status(Status(StatusCode.ERROR))
            if err:
                span.record_exception(err)
            
            # End span
            span.end()
            del self._active_spans[id_]
        
        return None
    
def instrument_opentelemetry(dispatcher_name: str = "root", tracer_name: str = "llama_index") -> None:
    """Instrument LlamaIndex to use OpenTelemetry."""
    event_handler = OpenTelemetryEventHandler(tracer_name=tracer_name)
    span_handler = OpenTelemetrySpanHandler(tracer_name=tracer_name)
    
    dispatcher = get_dispatcher(dispatcher_name)
    dispatcher.add_event_handler(event_handler)
    dispatcher.add_span_handler(span_handler)
