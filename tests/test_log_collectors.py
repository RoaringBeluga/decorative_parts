import random

import pytest

from decorative_parts import SimpleLogCollector, timed

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

@pytest.mark.parametrize('a_position,a_num', _nums.items())
def test_log_collector_protocol(a_position: str, a_num: int) -> None:
    """Test randomized logged run"""
    collector = DummyLogCollector()

    @timed(log_callback=collector, message_template="An Message", a_dog='A Pug!', a_cat='Manul',)
    def looper(rnd: int=1_000_000) -> None:
        for _ in range(rnd):
            pass

    looper(a_num)
    print(collector.get_logs())
    assert collector.counter != 0
    assert collector.get_logs() != ''

@pytest.mark.parametrize('a_position,a_num', _nums.items())
def test_simple_log_collector(a_position: str, a_num: int) -> None:
    """Test randomized logged run"""
    collector = SimpleLogCollector()

    @timed(log_callback=collector, message_template="An Message", a_dog='A Pug!', a_cat='Manul',)
    def looper(rnd: int=1_000_000) -> None:
        for _ in range(rnd):
            pass

    looper(a_num)
    print(collector.get_logs())
    assert collector.get_logs() != ''
    assert f'{collector}' != ''
