from .task import Task
from server.core.log import Log
from server.core.config import config
from server.database.repositories import DownloadRepository

import glob

log = Log.get_logger(__name__)


class TorrentFileHandler:
    @staticmethod
    def _is_torrent_file(path):
        return path.endswith(".torrent")

    def handle_file(self, path):
        if TorrentFileHandler._is_torrent_file(path):
            id = DownloadRepository.compute_id_from_torrent(path)
            log.info(f"{path} found")
            log.debug(f"Download ID is {id}")
            model = DownloadRepository.get_model(id)
            if model == None:
                log.debug(f"Adding {id} to database")
                DownloadRepository.create_model_from_torrent(path)
            else:
                log.debug(f"{id} already in database")


class TaskTorrentFiles(Task):
    async def run(self):
        holes_path = config.data_dir + "/holes"
        torrents = glob.glob(holes_path + "/**/*.torrent")
        handler = TorrentFileHandler()
        for f in torrents:
            handler.handle_file(f)
