from functools import wraps
from typing import Callable, Generator, ParamSpec, TypeVar, overload


P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


def yuck(
        func: Callable[P, Generator[T, U, V]]
    ) -> Callable[P, Generator[T, U, V]] | Callable[[], T | U] | Callable[[U], T | V]:
    @overload
    def wrapper() -> T | V: ...
    @overload
    def wrapper(value: U) -> T | V: ...
    @overload
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Generator[T, U, V]: ...

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        if not hasattr(wrapper, "__state_of_yuck__"):
            wrapper.__state_of_yuck__ = func(*args, **kwargs)
            return next(wrapper.__state_of_yuck__)
        
        value, *_ = args if args else (None,)
        try:
            return wrapper.__state_of_yuck__.send(value)
        except StopIteration:
            del wrapper.__state_of_yuck__

    return wrapper


__all__ = ["yuck"]
