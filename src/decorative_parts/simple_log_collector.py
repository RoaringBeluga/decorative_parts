from datetime import datetime


class SimpleLogCollector:

    def __init__(self, ):
        self._logs: dict[str, str] = {}

    def collect(self, **kwargs):
        key = datetime.now().isoformat()
        msg = kwargs.pop("msg", str(kwargs))
        self._logs[key] = msg.format(**kwargs)

    def get_logs(self) -> dict[str, str]:
        return self._logs

    def __str__(self) -> str:
        result = ""
        for key, value in self._logs.items():
            result += f"[{key}]: {value}\n"
        return result