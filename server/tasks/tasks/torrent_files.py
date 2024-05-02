from ..task import Task
from server.core import config
from server.core.log import Log
from server.database.repositories import (
    DownloadRepository,
)
from server.core.db import db

import glob
import os
from sqlalchemy.orm import Session

log = Log.get_logger(__name__)


class TorrentFileHandler:
    @staticmethod
    def _is_torrent_file(path):
        return path.endswith(".torrent")

    def __init__(self, session: Session):
        self._db_session = session
        self._download_repository = DownloadRepository(self._db_session)

    def handle_file(self, path):
        if TorrentFileHandler._is_torrent_file(path):
            id = DownloadRepository.compute_id_from_torrent(path)
            log.info(f"{path} found")
            log.debug("Download ID is " + str(id))
            model = self._download_repository.get_model(id)
            if model is None:
                log.debug(f"Adding {id} to database")
                model = self._download_repository.create_model_from_torrent(path)
            else:
                log.debug(f"{id} already in database")
            self._delete_torrent_file(path)

    def _delete_torrent_file(self, path):
        os.remove(path)


class TaskTorrentFiles(Task):
    async def run(self):
        self._db_session = db.new_scoped_session()
        holes_path = config.data_dir + "/holes"
        torrents = glob.glob(holes_path + "/**/*.torrent")
        handler = TorrentFileHandler(self._db_session)
        for f in torrents:
            handler.handle_file(f)
