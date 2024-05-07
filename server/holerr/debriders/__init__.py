from holerr.core import config

class WrappedDebrider():
    def __init__(self) -> None:
        self.update()

    def update(self):
        if config.debrider.real_debrid:
            from .real_debrid import RealDebrid

            self._debrider = RealDebrid(config.debrider.real_debrid)
        else:
            self._debrider = None

    def __getattr__(self, name):
        if self._debrider is None:
            raise Exception("No debrider found")
        return getattr(self._debrider, name)

debrider = WrappedDebrider()
