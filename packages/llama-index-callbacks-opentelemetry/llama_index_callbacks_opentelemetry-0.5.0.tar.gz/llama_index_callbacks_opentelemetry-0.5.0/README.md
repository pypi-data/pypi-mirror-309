# LlamaIndex Callback Integration: OpenTelemetry

```shell
pip install llama-index-callbacks-opentelemetry
```

## Usage

```python
from llama_index.core import set_global_handler

set_global_handler("opentelemetry")
```

or:

```python
from llama_index.callbacks.opentelemetry import instrument_opentelemetry

instrument_opentelemetry()
```
