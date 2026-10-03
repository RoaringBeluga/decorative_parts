import logging

from decorative_parts.timed_execution import timed

__all__ = [
    'timed',
    'info'
]


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
    Takes the following keyword arguments:
    """

def info() -> None:
    print(info_dump)
