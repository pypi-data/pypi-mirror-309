from __future__ import annotations

from typing import Callable
from json import dumps


def funcOrClassToStr(func: Callable | type) -> str:
    assert isinstance(func, Callable) or isinstance(func, type)
    f = getattr(func, '__name__', 'Unknown') if isinstance(func, Callable) else func
    return (getattr(func, '__name__', 'Unknown') + " contructor") if isinstance(func, type) else f


def kvargsToStr(kvargs: dict) -> str:
    d = dumps(kvargs)
    d = d.lstrip('{')
    return ", " + d.rstrip('}') if len(d) > 0 else ''


def argsToStr(args: tuple) -> str:
    a = ', '.join(map(lambda v: str(v), args)) if len(args) > 0 else ''
    return ", " + a if len(a) > 0 else ''