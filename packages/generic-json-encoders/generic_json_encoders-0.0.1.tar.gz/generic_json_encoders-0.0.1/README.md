# generic-json-encoders

A speedier version of the lilya encoders with more correct results and support for pydantic and msgspec.
It uses under the hood orjson.

[![PyPI - Version](https://img.shields.io/pypi/v/generic-json-encoders.svg)](https://pypi.org/project/generic-json-encoders)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/generic-json-encoders.svg)](https://pypi.org/project/generic-json-encoders)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install generic-json-encoders
```

## Usage

``` python
import datetime
from decimal import Decimal
from generic_json_encoders import json_encode, simplify

test_obj = {
    "datetime": datetime.datetime.now(),
    "date": datetime.date.today(),
    "decimal": Decimal("0.3").
}

# get json byte string
print(json_encode(test_obj))
# get simplified json serializable object
print(json_encode(test_obj))
```

### Integrating in lilya

Put somewhere in the init code of your application

``` python
from importlib import import_module
from contextlib import suppress

...
with suppress(ImportError):
    import_module("generic_json_encoders.lilya_monkey_patcher")
...

```


## License

`generic-json-encoders` is distributed under the terms of the [BSD](https://spdx.org/licenses/BSD-3-Clause.html) license.
