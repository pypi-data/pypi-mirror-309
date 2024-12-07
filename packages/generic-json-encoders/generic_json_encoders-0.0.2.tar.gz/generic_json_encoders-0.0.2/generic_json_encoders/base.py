from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Callable, Generator, Iterable
from contextlib import suppress
from dataclasses import asdict, is_dataclass
from functools import partial
from inspect import isclass
from typing import Any, Generic, TypeVar, cast

import orjson

IN = TypeVar("IN")
OUT = TypeVar("OUT")
APPLIED = TypeVar("APPLIED")


class Skip(BaseException):
    pass


def _no_transform(obj: Any) -> Any:
    return obj


class Encoder(ABC, Generic[IN, OUT, APPLIED]):
    """
    The base class for any custom encoder
    added to the system.
    """

    @abstractmethod
    def serialize(self, obj: IN) -> OUT:
        """Serialize or skip"""

    def apply_annotation(
        self, obj: Any, annotation: Any = None, transform_fn: Callable[[Any], Any] = _no_transform
    ) -> APPLIED:
        raise Skip


class StructureEncoder(Encoder):
    def __init__(
        self, types: tuple[type, ...] = (set, frozenset, Generator, Iterable, deque)
    ) -> None:
        self.types = types

    def serialize(self, obj: Any) -> list:
        if not isinstance(obj, self.types):
            raise Skip
        return list(cast(Any, obj))

    def apply_annotation(
        self, obj: Any, annotation: Any = None, transform_fn: Callable[[Any], Any] = _no_transform
    ) -> list:
        if not isclass(annotation) or not issubclass(annotation, list):
            raise Skip
        return list(transform_fn(obj))


class NamedTupleEncoder(Encoder):
    def serialize(self, obj: Any) -> dict:
        if not isinstance(obj, tuple) or not hasattr(obj, "_asdict"):
            raise Skip
        return cast(dict, obj._asdict())

    def apply_annotation(
        self, obj: Any, annotation: Any = None, transform_fn: Callable[[Any], Any] = _no_transform
    ) -> Any:
        if (
            not isclass(annotation)
            or not issubclass(annotation, tuple)
            or not hasattr(annotation, "_asdict")
        ):
            raise Skip
        if isinstance(obj, tuple) and hasattr(obj, "_asdict"):
            return obj
        obj = transform_fn(obj)
        if isinstance(obj, dict):
            return annotation(**obj)
        return annotation(*obj)


class DataclassEncoder(Encoder):
    def serialize(self, obj: Any) -> dict:
        # this will be probably not executed because of orjson handling it
        if isclass(obj) or not is_dataclass(obj):
            raise Skip
        return asdict(obj)

    def apply_annotation(
        self, obj: Any, annotation: Any = None, transform_fn: Callable[[Any], Any] = _no_transform
    ) -> Any:
        if not isclass(annotation) or not is_dataclass(annotation):
            raise Skip
        if not isclass(obj) and is_dataclass(obj):
            return obj
        obj = transform_fn(obj)
        return annotation(**obj)


class JSONEncodeEncoder(Encoder):
    def serialize(self, obj: Any) -> orjson.Fragment:
        if not hasattr(obj, "json_encode"):
            raise Skip
        return orjson.Fragment(obj.json_encode())


ENCODER_TYPES: deque[Encoder] = deque(
    [JSONEncodeEncoder(), StructureEncoder(), NamedTupleEncoder(), DataclassEncoder()]
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

    class MsgSpecEncoder(Encoder[Struct, orjson.Fragment, Struct]):
        def serialize(self, obj: Any) -> orjson.Fragment:
            """
            When a `msgspec.Struct` is serialised,
            it will call this function.
            """
            if not isinstance(obj, Struct):
                raise Skip()
            return orjson.Fragment(json.encode(obj))

        def apply_annotation(
            self,
            obj: Any,
            annotation: Any = None,
            transform_fn: Callable[[Any], Any] = _no_transform,
        ) -> Any:
            if not isclass(annotation) or not issubclass(annotation, Struct):
                raise Skip
            if isinstance(obj, Struct):
                return obj
            return json.decode(transform_fn(obj), type=annotation)

    register_encoder(MsgSpecEncoder())
except ImportError:
    pass


try:
    from pydantic import BaseModel

    class PydanticEncoder(Encoder[BaseModel, orjson.Fragment, BaseModel]):
        def serialize(self, obj: BaseModel) -> orjson.Fragment:
            if not isinstance(obj, BaseModel):
                raise Skip()
            return orjson.Fragment(obj.model_dump_json())

        def apply_annotation(
            self,
            obj: Any,
            annotation: Any = None,
            transform_fn: Callable[[Any], Any] = _no_transform,
        ) -> BaseModel:
            if not isclass(annotation) or not issubclass(annotation, BaseModel):
                raise Skip
            if isinstance(obj, BaseModel):
                return obj
            return annotation(**transform_fn(obj))

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


def json_encode(value: Any, **kwargs: Any) -> bytes:
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


def apply_annotation(
    value: Any, annotation: Any = None, *, transform_fn: Callable[[Any], Any] | None = None
) -> Any:
    if transform_fn is None:
        transform_fn = _no_transform
    for encoder in ENCODER_TYPES:
        with suppress(Skip):
            return encoder.apply_annotation(value, annotation, transform_fn=transform_fn)
    if isclass(annotation):
        if isinstance(value, annotation):
            return value
        return annotation(transform_fn(value))
    return value
