import logging

import pytest

from decorative_parts.logged_execution import logged, logger


class CustomTestException(RuntimeError):
    ...


def test_logged_with_defaults(caplog):
    """Test @logged decorator with defaults"""
    caplog.set_level(logging.DEBUG)
    arg_tuple = (0, '1', 'two',)
    kwarg_dict = {'dictionary_1': {1: '1', 2: '2', 3: '3'}, 'animal': "pig"}
    params = {'args': arg_tuple, 'kwargs': kwarg_dict}

    call_logged = False
    result_logged = False

    @logged
    def a_func(*args, **kwargs):
        return "Success"

    caplog.clear()
    result = a_func(*arg_tuple, **kwarg_dict)

    for record in caplog.records:
        assert record.msg is not None
        if 'called' in record.message:
            call_logged = True
            assert record.message == f"Function: {a_func.__name__} called.\nParameters:\n{params}"
        elif 'ran' in record.message:
            result_logged = True
            assert record.message == f"Function {a_func.__name__} ran successfully with result: {result}"

    assert call_logged and result_logged, f"Call logged: {call_logged}. Result logged: {result_logged}."


def test_logged_with_parameters(caplog):
    """Test @logged decorator with defaults"""
    caplog.set_level(logging.DEBUG)
    # Parameters for the decorated function
    arg_tuple = (0, '1', 'two',)
    kwarg_dict = {'dictionary_1': {1: '1', 2: '2', 3: '3'}, 'animal': "dog"}
    params = {'args': arg_tuple, 'kwargs': kwarg_dict}

    # Logging
    logger_name = 'new_logger'
    new_logger = logging.getLogger(logger_name)
    call_logged = False
    result_logged = False

    # Parameters for the decorator
    message_before = "Start: {func_name} likes a {dog}"
    message_after = "Done: {func_name} completed liking a {dog} with the result: {result}"
    message_error = "Fail: {func_name} raised an error while petting a {dog}: {err}"
    dog = "Pug"

    @logged(logger=new_logger, level=logging.INFO,
            message_before=message_before,
            message_after=message_after,
            message_error=message_error,
            dog=dog)
    def a_func(*args, **kwargs):
        return "Success"

    caplog.clear()
    result = a_func(*arg_tuple, **kwarg_dict)

    for record in (record for record in caplog.records if record.name == logger_name):
        assert record.msg is not None
        if 'Start: ' in record.message:
            call_logged = True
            assert record.message == message_before.format(func_name=a_func.__name__, params=params, dog=dog)
        elif 'Done: ' in record.message:
            result_logged = True
            assert record.message == message_after.format(func_name=a_func.__name__, dog=dog, result=result)

    assert call_logged and result_logged, f"Call logged: {call_logged}. Result logged: {result_logged}."


def test_logged_with_parameters_error(caplog):
    """Test @logged decorator with defaults"""
    caplog.set_level(logging.DEBUG)

    arg_tuple = (0, '1', 'two',)
    kwarg_dict = {'dictionary_1': {1: '1', 2: '2', 3: '3'}, 'animal': "dog"}
    params = {'args': arg_tuple, 'kwargs': kwarg_dict}

    logger_name = 'new_logger'
    new_logger = logging.getLogger(logger_name)
    call_logged = False
    failure_logged = False

    message_before = "Start: {func_name} likes a {dog}"
    message_after = "Done: {func_name} completed liking a {dog} with the result: {result}"
    message_error = "Fail: {func_name} raised an error while petting a {dog}: {err}"
    dog = "Pug"

    @logged(logger=new_logger, level=logging.INFO,
            message_before=message_before,
            message_after=message_after,
            message_error=message_error,
            dog=dog)
    def a_func(*args, **kwargs):
        raise CustomTestException("Exceptional")

    caplog.clear()
    with pytest.raises(CustomTestException) as err:
        result = a_func(*arg_tuple, **kwarg_dict)
    assert err.type == CustomTestException

    for record in (record for record in caplog.records if record.name == logger_name):
        assert record.msg is not None

        if 'Start: ' in record.message:
            call_logged = True
            assert record.message == message_before.format(func_name=a_func.__name__, params=params, dog=dog)
        elif 'Fail: ' in record.message:
            assert record.levelno == logging.ERROR
            failure_logged = True
            assert record.message == message_error.format(func_name=a_func.__name__, dog=dog, err=err.value)
        elif 'Done: ' in record.message:
            assert record.message == message_after.format(func_name=a_func.__name__, dog=dog, result=result)
            assert False, "Received run result where none was expected"

    assert call_logged and failure_logged, "Logging error. Call logged: {call_logged}. Failure logged: {failure_logged}."


def test_logger_decorator(caplog):
    """Test @logged decorator with defaults"""
    caplog.set_level(logging.INFO)

    @logger
    def a_func(*args, **kwargs):
        return 'Success'

    an_arg = ('owl!',)
    kwa = {'one': 1, 'two': 2}
    caplog.clear()
    result = a_func(*an_arg, **kwa)

    for record in caplog.records:
        assert record.message is not None
        if 'with args' in record.message:
            assert record.message == f"Running {a_func.__name__} with args: {an_arg}, kwargs: {kwa}"
        elif 'with result' in record.message:
            assert record.message == f"Finished {a_func.__name__} with result: {result}"


def test_logger_decorator_error(caplog):
    """Test @logged decorator with defaults"""
    caplog.set_level(logging.INFO)

    @logger
    def a_func(*args, **kwargs):
        raise CustomTestException("Exceptional")

    an_arg = ('owl!',)
    kwa = {'one': 1, 'two': 2}
    caplog.clear()

    with pytest.raises(CustomTestException) as err:
        a_func(*an_arg, **kwa)
    assert err.type == CustomTestException
    assert "Exceptional" in str(err.value)

    for record in caplog.records:
        assert record.message is not None
        if 'Error' in record.message:
            assert record.levelno == logging.ERROR
            assert "Exceptional" in record.message
