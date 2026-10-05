import copy
import logging
from typing import Any

import pytest

from decorative_parts.timed_execution import timed

_DEBUG = False

_test_data = [
    (0, "Test zero"),
    (1_000_000, "Test a million"),
    (10_000_000, "Test ten millions"),
    (100_000_000, "Test hundred millions"),
]

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class _DataCollector:
    def __init__(self) -> None:
        self.msg = None
        self.start = 0
        self.end = 0
        self.diff = -1
        self.func_name = "<Unknown>"
        self.extra_args: dict[str, Any] = {}

    def log_capture(self, **kwargs) -> None:
        temp = copy.copy(kwargs)
        if _DEBUG: print("Keyword args: ", temp)
        self.extra_args = temp.pop('extra', {})
        if _DEBUG: print("Extra args: ", self.extra_args)
        self.msg: str = temp.pop('msg', None).format(**self.extra_args)
        self.start = temp.pop('start', None)
        self.end = temp.pop('end', 0)
        self.func_name = temp.pop('func_name', "<Unknown>")
        self.diff = temp.pop('diff', -1)

    @property
    def seconds(self) -> int:
        return int(self.diff / 1_000_000_000)

    @property
    def milliseconds(self) -> int:
        return int(self.diff / 1_000_000)

    @property
    def diff_str(self) -> str:
        nanos_s = self.seconds * 1_000_000_000
        nanos_ms = self.milliseconds * 1_000_000
        return f"{nanos_s}.{self.diff - nanos_s}s"


@pytest.mark.asyncio
@pytest.mark.parametrize('iterations, test_message', _test_data)
async def test_timed_annotation_with_parameters(iterations: int, test_message: str) -> None:
    """Tests the basic functionality and parameter passing of @timed with custom logger."""

    collector = _DataCollector()

    # Use the collector's method as the logger function, passing all necessary metrics.
    @timed(logger_func=collector.log_capture, message_template="{message}", message=test_message)
    async def a_func(repetitions: int):
        acc: int = 0
        for i in range(repetitions):
            acc = acc + i if i % 2 == 0 else acc - int(i / 2)

    await a_func(iterations)

    # Assertions check that the decorated function was called and correctly logged metrics.
    assert collector.msg == test_message
    assert "a_func" in collector.func_name  # Check name capture
    assert collector.start is not None
    assert collector.end is not None
    assert collector.diff > 0


@pytest.mark.asyncio
@pytest.mark.parametrize('iterations,test_message', _test_data)
async def test_async_timed_decorator(capsys, caplog, iterations: int, test_message: str) -> None:
    """Tests the default behavior of @timed."""
    logger = logging.getLogger('PP_duster')
    logger.setLevel(logging.INFO)

    @timed
    async def a_func(repetitions: int):
        acc: int = 0
        for i in range(repetitions):
            acc = acc + i if i % 2 == 0 else acc - int(i / 2)
        logger.info(test_message)
        _logger.info(test_message)

    _ = await a_func(iterations)

    test_output = capsys.readouterr()

    assert "Function: a_func runtime " in test_output.out
    _logger.info(f"Capsys: {test_output.out}")
