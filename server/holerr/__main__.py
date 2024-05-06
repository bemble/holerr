
#------------------------------------------------------------------------------
# Init
# Not called in __init__.py because of alembic importing holerr.database
#------------------------------------------------------------------------------
from holerr.core import config

config.load()

from holerr.core.log import Log

log = Log.get_logger(__name__)

from holerr.core.config_repositories import PresetRepository

PresetRepository.create_watch_directories()

from holerr.debriders import debrider

if not debrider.is_connected():
    log.info("Debrider not connected")

from holerr.downloaders import downloader

if not downloader.is_connected():
    log.info("Downloader not connected")


#------------------------------------------------------------------------------
# Main itself
#------------------------------------------------------------------------------
from holerr.tasks import worker
from holerr.api import server
import sys

def main() -> int:
    worker.start()
    server.start()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        worker.stop()
