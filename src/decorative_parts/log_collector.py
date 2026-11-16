from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class LogCollector(Protocol):
    def collect(self, **kwargs) -> None: ...
    def get_logs(self) -> dict[str, str]: ...