from rapidx.app.data.db.db import Db
from rapidx.app.data.progresssignal import ProgressSignal


class Loader:
    def __init__(self) -> None:
        self._signal = ProgressSignal()

    def signal(self) -> ProgressSignal:
        return self._signal    
