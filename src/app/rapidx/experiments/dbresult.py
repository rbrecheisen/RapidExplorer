from typing import Any
from concurrent.futures import Future


class DbResult(Future):
    def __init__(self) -> None:
        super(DbResult, self).__init__()

    def get(self) -> Any:
        return self.result()

    def set(self, obj: Any):
        self.set_result(obj)

    def setException(self, obj: Any):
        self.set_exception(obj)
