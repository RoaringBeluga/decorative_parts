"""Decorator for timing execution of functions"""
import functools
from time import perf_counter_ns
from typing import Any, Callable


def _printout(**kwargs) -> None:
    """Default logging function. Prints the message to the stdout, formatting it."""
    message = kwargs.get('msg', '')
    print(message.format(**kwargs))


def timed(function = None, /, *, logger_func: Callable[..., Any] = _printout,
          message_template: str = "Function: {func_name} runtime {diff} nanoseconds",
          **decorator_args) -> Callable[..., Callable[..., Any]]:
    """Timed execution decorator

    :param logger_func: logging callback function
    :param message_template: message template to be passed to the callback
    :param decorator_args: additional arguments to be passed to the callback function
    :return: decorated function
    """
    def outer(func):
        @functools.wraps(func)
        def inside(*args, **kwargs):
            func_name = func.__name__
            start = perf_counter_ns()
            res = func(*args, **kwargs)
            end = perf_counter_ns()
            diff = end - start
            logger_func(msg=message_template, func_name=func_name, start=start, end=end, diff=diff,
                        extra=decorator_args)
            return res
        return inside

    if callable(function):
        return outer(function)
    return outer
