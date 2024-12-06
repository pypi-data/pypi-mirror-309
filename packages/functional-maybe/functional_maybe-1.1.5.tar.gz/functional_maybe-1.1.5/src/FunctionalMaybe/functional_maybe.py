from __future__ import annotations

import copy
import traceback
import sys
from .formatting import *
from .empty import Empty

from typing import TypeVar, Generic, Callable, Union, Any

T = TypeVar('T')
V = TypeVar('V')


class FunctionalMaybe(Generic[T]):
    """
        Wraps given value to which it can transform to different values and can run given
        functions with the wrapped value.
    """

    Unwrapper = object()

    def __init__(self, v: T = None, **kvargs):
        """
        Create wrapper 'Maybe[T]' for a given value of type T.
        :param v: Value to be wrapped
        """

        self.v: T = v
        if 'funcCallTrace' in kvargs:
            self.trace = kvargs['funcCallTrace']
        else:
            self.trace = []
            self.__add_to_trace(f"Constructor({v})")

    def __mapArgsKvargs(self, *args, **kvargs):
        """Function to map all instances of FunctionalMaybe.Unwrapper to self.v

        :param args: All non-keyword arguments
        :param kvargs: All keyword arguments
        :return: args, kvargs
        """
        args = tuple(map(lambda val: self.v if val == FunctionalMaybe.Unwrapper else val, args))
        for k, v in kvargs.items():
            if v == FunctionalMaybe.Unwrapper:
                kvargs[k] = self.v
        return args, kvargs

    def __add_to_trace(self, what: str) -> None:
        """Add given string detailing a function call to the end of the trace
        :param what: A string describing a function call
        """
        self.trace.append(what)

    def construct(self, type_: V, dontSupply: bool = True, *args, **kvargs) -> FunctionalMaybe[V]:
        """
        Construct an object of type_ and with params and return as Maybe

        :param type_: Type of object to be created
        :param dontSupply: Boolean flag for if we want to suply the wrapped value as the first argument to f or not
        :return: A maybe of type_ with parameters params
        """
        self.__add_to_trace(f"Construct({funcOrClassToStr(type_)}, {dontSupply}{argsToStr(args)}{kvargsToStr(kvargs)})")

        args, kvargs = self.__mapArgsKvargs(*args, **kvargs)

        def construct(*a, **kv):
            return type_(*a, **kv)

        return self.transform(construct, dontSupply, *args, **kvargs)

    def apply(self, f: Callable[[T, ...], V] | Callable[[...], V], dontSupply: bool = False, *args, **kvargs) \
            -> Union[V, Empty]:
        """Apply the wrapped variable to a given function and return the value or an Empty.

        :param f: The function to be applied
        :param dontSupply: Boolean flag for if we want to suply the wrapped value as the first argument to f or not
        :return: result of the wrapped value given to f
        """
        if not isinstance(dontSupply, bool):
            raise ValueError("Don't supply was not a boolean!")
        args, kvargs = self.__mapArgsKvargs(*args, **kvargs)

        # Create deepcopy incase this alters self.v
        value = copy.deepcopy(self.v)
        if bool(self):
            try:
                return f(value, *args, **kvargs) if not dontSupply else f(*args, **kvargs)
            except Exception as exp:
                stack_trace = traceback.format_stack()
                stack_trace.reverse()
                return Empty(
                    previousValue=value,
                    reason=str(exp) + f". Traceback:\n{''.join(stack_trace)}"
                )

    def transform(self, f: Callable[[T, ...], V] | Callable[[...], V], dontSupply: bool = False, *args, **kvargs) \
            -> FunctionalMaybe[Union[V, Empty]]:
        """Apply the given function and wrap the value in a new Maybe

        :param f: Function to be applied
        :param dontSupply: Boolean flag for if we want to suply the wrapped value as the first argument to f or not
        :return: A new maybe wrapping the result of the application of f
        """
        self.__add_to_trace(f"Transform({funcOrClassToStr(f)}, {dontSupply}{argsToStr(args)}{kvargsToStr(kvargs)})")
        return FunctionalMaybe(self.apply(f, dontSupply, *args, **kvargs), funcCallTrace=self.trace)

    def transformers(self, *f: Callable[[T], V] | Callable[[Any], V]) \
            -> FunctionalMaybe[Union[V, Empty]]:
        """Apply the given functions and wrap the value in a new Maybe

        :param f: Functions to be applied in an iterable
        :return: A new maybe wrapping the result of the application of f
        """
        # No functions:
        if not len(f):
            return self
        self.__add_to_trace(f"Transformers{tuple(map(funcOrClassToStr, f))}")
        r = FunctionalMaybe(self.v, funcCallTrace=self.trace)
        for f_ in f:
            r = r.transform(f_)
        return r

    def run(self, f: Callable[[T, ...], V] | Callable[[...], V], dontSupply: bool = False, *args, **kvargs)\
            -> FunctionalMaybe[T]:
        """Run function f and if it results in an exception print the info to console

        :param f: Function to be run on the wrapped value
        :param dontSupply: Boolean flag for if we want to suply the wrapped value as the first argument to f or not
        :return: self
        """
        args, kvargs = self.__mapArgsKvargs(*args, **kvargs)
        self.__add_to_trace(f"Run({funcOrClassToStr(f)}, {dontSupply}{argsToStr(args)}{kvargsToStr(kvargs)})")
        val: V = self.apply(f, dontSupply, *args, **kvargs)
        if isinstance(val, Empty):
            print(val, file=sys.stderr)
        return self

    def runners(self, *f: Callable[[T], V]) -> FunctionalMaybe[T]:
        """Run function f and if it results in an exception print the info to console

                :param f: Function to be run on the wrapped value
                :return: self
                """
        self.__add_to_trace(f"Runners({tuple(map(funcOrClassToStr, f))})")
        for f_ in f:
            val: V = self.apply(f_)
            if isinstance(val, Empty):
                print(val, file=sys.stderr)
        return self

    def unwrap(self) -> T:
        """Get the wrapped value

        :return: The wrapped value
        """
        return self.v

    def orElse(self, something: V) -> Union[T, V]:
        """Get the wrapped value or something else
        if the Maybe contained an Empty.

        :param something: What to return incase of an Empty.
        :return: Wrapped value or the provided value.
        """
        return self.v if not isinstance(self.v, Empty) else something

    def __bool__(self) -> bool:
        """Is the wrapped value an empty

        :return: True if the wrapped value is an empty
        """
        return not isinstance(self.v, Empty)

    def __str__(self) -> str:
        """Convert to string

        :return: String representing the structure of the Maybe
        """
        return "Maybe[ value:" + type(self.v).__name__ + " = " + str(self.v) + " ]"
