from typing import Any

from lilya.encoders import Encoder, register_encoder

from .base import simplify


class InjectedGenericJsonEncoder(Encoder):
    def is_type(self, value: Any) -> bool:
        return True

    def serialize(self, obj: Any) -> Any:
        return simplify(obj)


register_encoder(InjectedGenericJsonEncoder())
