from dataclasses import dataclass
from typing import Any, Callable

from briton.proto import InferenceRequest


@dataclass
class InferParams:
    briton_stub: Any
    briton_request: InferenceRequest
    model_input: dict
    generate_request_id: Callable[[], str]
    tokenizer: Any
    stream: bool
