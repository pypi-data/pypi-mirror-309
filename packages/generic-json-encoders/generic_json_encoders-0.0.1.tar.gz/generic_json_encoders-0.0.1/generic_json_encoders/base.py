from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Callable, Generator, Iterable
from contextlib import suppress
from functools import partial
from typing import Any, Generic, TypeVar, cast

import orjson

IN = TypeVar("IN")
OUT = TypeVar("OUT")


class Skip(BaseException):
    pass


class Encoder(ABC, Generic[IN, OUT]):
    """
    The base class for any custom encoder
    added to the system.
    """

    @abstractmethod
    def serialize(self, obj: IN) -> OUT:
        """Serialize or skip"""


class StructureEncoder(Encoder):
    def serialize(self, obj: Any) -> list[Any]:
        if not isinstance(obj, (set, frozenset, Generator, Iterable, deque)):
            raise Skip
        return list(obj)


class NamedTupleEncoder(Encoder):
    def serialize(self, obj: Any) -> dict:
        if not isinstance(obj, tuple) or not hasattr(obj, "_asdict"):
            raise Skip
        return cast(dict, obj._asdict())


class JSONEncodeEncoder(Encoder):
    def serialize(self, obj: Any) -> orjson.Fragment:
        if not hasattr(obj, "json_encode"):
            raise Skip
        return orjson.Fragment(obj.json_encode())


ENCODER_TYPES: deque[Encoder] = deque(
    [
        JSONEncodeEncoder(),
        StructureEncoder(),
        NamedTupleEncoder(),
    ]
)


def register_encoder(encoder: Encoder) -> None:
    remove_elements: list[Encoder] = []
    for value in ENCODER_TYPES:
        if value.__class__ == encoder.__class__:
            remove_elements.append(value)
    for element in remove_elements:
        ENCODER_TYPES.remove(element)
    ENCODER_TYPES.appendleft(encoder)


try:
    from msgspec import Struct, json

    class MsgSpecEncoder(Encoder[Struct, orjson.Fragment]):
        def serialize(self, obj: Any) -> orjson.Fragment:
            """
            When a `msgspec.Struct` is serialised,
            it will call this function.
            """
            if not isinstance(obj, Struct):
                raise Skip()
            return orjson.Fragment(json.encode(obj))

    register_encoder(MsgSpecEncoder())
except ImportError:
    pass


try:
    from pydantic import BaseModel

    class PydanticEncoder(Encoder[BaseModel, orjson.Fragment]):
        def serialize(self, obj: BaseModel) -> orjson.Fragment:
            if not isinstance(obj, BaseModel):
                raise Skip()
            return orjson.Fragment(obj.model_dump_json())

    register_encoder(PydanticEncoder())
except ImportError:
    pass


def _raise_error(value: Any) -> None:
    raise ValueError(f"Object of type '{type(value).__name__}' is not JSON serializable.")


def _parse_extra_type(value: Any, *, chained: Callable[[Any], Any]) -> Any:
    for encoder in ENCODER_TYPES:
        with suppress(Skip):
            return encoder.serialize(value)
    try:
        chained(value)
    except ValueError:
        return str(value)


def json_encode(value: Any, annotation: Any = None, **kwargs: Any) -> bytes:
    """
    Encode a value to a JSON-compatible format using a list of encoder types.

    Parameters:
    value (Any): The value to encode.

    Returns:
    bytes: The JSON encoded value.

    Raises:
    ValueError: If the value is not serializable by any provided encoder type.
    """
    chained = kwargs.pop("default", _raise_error)
    kwargs.setdefault("option", orjson.OPT_SERIALIZE_NUMPY)
    return orjson.dumps(
        value,
        default=partial(_parse_extra_type, chained=chained),
        **kwargs,
    )


def simplify(value: Any, **kwargs: Any) -> Any:
    """
    Parameters:
    value (Any): The value to encode.

    Returns:
    Any: The JSON-compatible encoded value.
    """
    return orjson.loads(json_encode(value, **kwargs))
