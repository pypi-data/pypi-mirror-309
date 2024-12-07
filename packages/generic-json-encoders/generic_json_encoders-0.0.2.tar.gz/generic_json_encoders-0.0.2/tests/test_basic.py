import datetime
import math
from dataclasses import dataclass
from decimal import Decimal
from functools import partial
from typing import NamedTuple

import pytest

from generic_json_encoders import apply_annotation, json_encode, simplify

test_obj = {
    "datetime": datetime.datetime(year=2024, month=9, day=12),
    "date": datetime.date(year=1990, month=1, day=1),
    "decimal": Decimal("0.3"),
    "float": 0.4,
    "inf": math.inf,
}


@pytest.mark.parametrize(
    "inp,result",
    [
        (Decimal("0.343430000000988"), b'"0.343430000000988"'),
        (
            test_obj,
            b'{"datetime":"2024-09-12T00:00:00","date":"1990-01-01","decimal":"0.3","float":0.4,"inf":null}',
        ),
    ],
)
def test_json_encode(inp, result):
    assert json_encode(inp) == result


@pytest.mark.parametrize(
    "inp,result",
    [
        (Decimal("0.343430000000988"), "0.343430000000988"),
        (
            test_obj,
            {
                "datetime": "2024-09-12T00:00:00",
                "date": "1990-01-01",
                "decimal": "0.3",
                "float": 0.4,
                "inf": None,
            },
        ),
    ],
)
def test_json_simplify(inp, result):
    assert simplify(inp) == result


def test_monkey_patching():
    from lilya.encoders import ENCODER_TYPES

    from generic_json_encoders.lilya_monkey_patcher import GenericJsonEncoder

    assert ENCODER_TYPES[0].__class__ is GenericJsonEncoder
    assert ENCODER_TYPES[0].serialize(True) is True
    assert ENCODER_TYPES[0].serialize(datetime.date(year=2024, month=12, day=1)) == "2024-12-01"


class Foo(NamedTuple):
    decimal: Decimal
    str_list: list[str]


@dataclass
class Foo2:
    decimal: Decimal
    str_list: list[str]


def test_apply_annotation():
    assert apply_annotation("92.24232", Decimal) == Decimal("92.24232")
    assert apply_annotation("2.333", Decimal, transform_fn=partial(simplify)) == Decimal("2.333")
    assert apply_annotation((Decimal("92.24232"), ("test", "test")), Foo) == Foo(
        decimal=Decimal("92.24232"), str_list=("test", "test")
    )
    assert apply_annotation(
        {"decimal": Decimal("92.24232"), "str_list": ("test", "test")}, Foo2
    ) == Foo2(decimal=Decimal("92.24232"), str_list=("test", "test"))

    assert apply_annotation(("test", "test"), list) == ["test", "test"]
    # passthrough
    assert apply_annotation(Decimal("2.333"), transform_fn=partial(simplify)) == Decimal("2.333")
