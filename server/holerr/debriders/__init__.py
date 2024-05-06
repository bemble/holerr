from holerr.core import config
from .debrider import Debrider

debrider: Debrider | None = None

if config.debrider.real_debrid:
    from .real_debrid import RealDebrid

    debrider = RealDebrid(config.debrider.real_debrid)

if debrider is None:
    raise Exception("No debrider found")
