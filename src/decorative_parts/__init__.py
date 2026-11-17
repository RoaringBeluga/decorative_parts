

__all__ = [
    'LogCollector',
    'SimpleLogCollector',
    'info',
    'logged',
    'timed',
]

from decorative_parts.log_collector import LogCollector
from decorative_parts.logged_execution import logged
from decorative_parts.simple_log_collector import SimpleLogCollector
from decorative_parts.timed_execution import timed

info_dump = """### Decorators:
    @timed
    Times the function's execution
    Takes the following keyword arguments:
        logger_func: A function that receives the info with possible arguments:
            msg: str - message template
            func_name: str - name of the function executed
            start: int - function start time in nanoseconds
            end: int - function finishing time in nanoseconds
            diff: int - execution time in nanoseconds
            extra: dict[str, Any] - extra keyword arguments as passed to the decorator
        message_template: str - message template, defaults to "Function: {func_name} runtime {diff} nanoseconds"
        **decorator_args: arbitrary extra keyword arguments
    Default logger just prints out the function name and execution time in nanoseconds to stdout
    Example:
    
        @timed(logger_func=write_to_log, message_template="{func_name} ran for {diff} with extra one={one}", one=1)
        def a_func():
            for _ in range(100_000_000_000):
                pass
    
    @logged
    Writes to logs before and after the function'[s execution and on errors
    Log execution start, completion and errors
        logger: Logger instance, defaults to ``logging.getLogger(__name__)``
        level: Log level, defaults to ``logging.DEBUG``
        message_before: Log entry template for before the execution
        message_after: Log entry template for after the execution
        message_error: Log entry template for errors (log level ALWAYS set to ``logging.ERROR)``
        decorator_args: optional keyword arguments for the decorator
            String template reference:
                * ``{func_name}``: name of the decorated function. Built-in `funcName` is NOT correct
                * ``{params}``: Dictionary of parameters of the decorated function:
                - ``params['args']``: list of positional arguments
                - ``params['kwargs']``: dictionary of keyword arguments
                * ``{result}``: Function execution result
                * ``{err}``: Error raised during execution
    """


def info() -> None:
    print(info_dump)
