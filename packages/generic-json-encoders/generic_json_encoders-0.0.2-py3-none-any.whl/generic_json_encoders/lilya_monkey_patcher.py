from collections.abc import Callable
from typing import Any, Optional

from lilya.encoders import Encoder, register_encoder

from .base import apply_annotation, simplify


class GenericJsonEncoder(Encoder):
    def __init__(self, transform_fn: Optional[Callable[[Any], Any]] = None) -> None:
        self.transform_fn = transform_fn

    def is_type(self, value: Any) -> bool:
        return True

    def serialize(self, obj: Any) -> Any:
        return simplify(obj)

    def encode(self, annotation: Any, value: Any) -> Any:
        # for esmerald
        return apply_annotation(value, annotation, transform_fn=self.transform_fn)


register_encoder(GenericJsonEncoder())
# old alias
InjectedGenericJsonEncoder = GenericJsonEncoder
