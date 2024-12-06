# struct4py

![Unittest](https://github.com/ahartlba/struct4py/actions/workflows/testing.yml/badge.svg?branch=main)
![Static Badge](https://img.shields.io/badge/https%3A%2F%2Fimg.shields.io%2Fbadge%2Fcode%2520style-black-black?label=codestyle)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/decorator-validation)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

Matlab like structure for python

An example on how to use it in your workflow.
Functions like Matlab structs where you can directly assign multiple levels of data.

```py
from struct4py import Struct

# Example usage
data = Struct()

# Assigning primitive value
data.a = 10
print(data)  # Struct({'a': 10})
print(data.a)  # 10

data.b.c = 20
print(data.b.c)  # 20
print(data)  # Struct({'a': 10, 'b': Struct({'c': 20})})

data.a.c = 10  # will fail as data.a already exists
```
