from rapidx.app.data.progresssignal import ProgressSignal


class Factory:
    def __init__(self) -> None:
        self._signal = ProgressSignal()

    def signal(self) -> ProgressSignal:
        return self._signal    
