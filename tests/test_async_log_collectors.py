import random

import pytest

from decorative_parts import timed, SimpleLogCollector

_nums = {
    '01': random.randrange(1_000_000_000),
    '02': random.randrange(1_000_000_000),
    '03': random.randrange(1_000_000_000),
    '04': random.randrange(1_000_000_000),
    '05': random.randrange(1_000_000_000),
    '06': random.randrange(1_000_000_000),
    '07': random.randrange(1_000_000_000),
    '08': random.randrange(1_000_000_000),
    '09': random.randrange(1_000_000_000),
    '10': random.randrange(1_000_000_000),
}

class DummyLogCollector:
    def __init__(self) -> None:
        self.counter: int = 0
        self._mess: str = ''

    def collect(self, **kwargs) -> None:
        self.counter += 1
        self._mess = self._mess + f"Line {self.counter} --> {kwargs}\n"

    def get_logs(self):
        return self._mess

@pytest.mark.asyncio
@pytest.mark.parametrize('a_position,a_num', _nums.items())
async def test_log_collector_protocol_async(a_position: str, a_num: int) -> None:
    """Test randomized logged run - async version, dummy logger"""
    collector = DummyLogCollector()

    @timed(log_callback=collector, message_template="An Message", a_dog='A Pug!', a_cat='Manul',)
    async def looper(rnd: int=1_000_000) -> None:
        for _ in range(0, rnd):
            pass

    await looper(a_num)
    print(collector.get_logs())
    assert collector.counter != 0
    assert collector.get_logs() != ''


@pytest.mark.asyncio
@pytest.mark.parametrize('a_position,a_num', _nums.items())
async def test_simple_log_collector(a_position: str, a_num: int) -> None:
    """Test randomized logged run - async version, SimpleLogCollector"""
    collector = SimpleLogCollector()

    @timed(log_callback=collector, message_template="An Message", a_dog='A Pug!', a_cat='Manul',)
    async def looper(rnd: int=1_000_000) -> None:
        for _ in range(0, rnd):
            pass

    await looper(a_num)
    print(collector.get_logs())
    assert collector.get_logs() != ''
    assert f'{collector}' != ''
