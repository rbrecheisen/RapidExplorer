from rapidx.app.plugins.plugin import Plugin


class TaskPlugin:
    def name(self) -> str:
        raise NotImplementedError('Not implemented')