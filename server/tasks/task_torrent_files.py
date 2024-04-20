from .task import Task
from server.core.log import Log
from server.core.config import config

import glob

log = Log.get_logger(__name__)


class TaskTorrentFiles(Task):
    async def run(self):
        log.debug("Torrent files task starting")
        holes_path = config.data_dir + "/holes"
        torrents = glob.glob(holes_path + "/**/*.torrent")
        for f in torrents:
            # add new torrents
            pass
