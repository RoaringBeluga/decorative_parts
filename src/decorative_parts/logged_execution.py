import functools
import logging


def logged(function = None, /, *, logger = logging.getLogger(__name__),
           level = logging.DEBUG,
           message_before: str = "Function: {func_name} called.\nParameters:\n{params}",
           message_after: str = "Function {func_name} ran successfully with result: {result}",
           message_error: str = "Function {func_name} raised an error: {err}",
          **decorator_args):
    """Log execution start, completion and errors
        String template reference:

        * ``{func_name}``: name of the decorated function. Built-in `funcName` is NOT correct
        * ``{params}``: Dictionary of parameters of the decorated function:
            - ``params['args']``: list of positional arguments
            - ``params['kwargs']``: dictionary of keyword arguments
        * ``{result}``: Function execution result
        * ``{err}``: Error raised during execution
    :param logger: Logger instance, defaults to ``logging.getLogger(__name__)``
    :param level: Log level, defaults to ``logging.DEBUG``
    :param message_before: Log entry template for before the execution
    :param message_after: Log entry template for after the execution
    :param message_error: Log entry template for errors (log level ALWAYS set to ``logging.ERROR)``
    :param decorator_args: optional keyword arguments for the decorator
    """
    def outer(func):
        @functools.wraps(func)
        def inside(*args, **kwargs):
            func_name = func.__name__
            extra = {**decorator_args,
                'func_name': func_name,
                 'params': {
                    'args': args,
                    'kwargs': kwargs,
                },
            }
            logger.log(level = level,msg=message_before.format(**extra), extra=extra)
            try:
                res = func(*args, **kwargs)
                extra['result'] = res
                logger.log(level = level,msg=message_after.format(**extra), extra=extra)
            except Exception as err:
                extra['err'] = err
                logger.log(level = logging.ERROR,msg=message_error.format(**extra), extra=extra)
                raise
            else:
                return res
        return inside

    if callable(function):
        return outer(function)
    return outer


def logger(func):
    """
    A basic decorator function to log information about function calls and their results.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        The wrapper function that logs function calls and their results.
        """
        logging.info(f"Running {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Finished {func.__name__} with result: {result}")
        except Exception as e:
            logging.error(f"Error occurred in {func.__name__}: {e}")
            raise
        else:
            return result
    return wrapper