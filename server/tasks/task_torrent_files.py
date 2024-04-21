from .task import Task
from server.core import config
from server.core.log import Log
from server.database.repositories import DownloadRepository, DebriderInfoRepository
from server.database.models import DownloadModel, DownloadStatus
from server.util.torrent import Torrent
from server.debriders import debrider
from server.core.db import db

import glob
import os

log = Log.get_logger(__name__)


class TorrentFileHandler:
    @staticmethod
    def _is_torrent_file(path):
        return path.endswith(".torrent")

    def __init__(self):
        self._db_session = db.new_scoped_session()
        self._download_repository = DownloadRepository()
        self._download_repository.set_session(self._db_session)
        self._debrider_info_repository = DebriderInfoRepository()
        self._debrider_info_repository.set_session(self._db_session)

    def handle_file(self, path):
        if TorrentFileHandler._is_torrent_file(path):
            id = DownloadRepository.compute_id_from_torrent(path)
            log.info(f"{path} found")
            log.debug(f"Download ID is {id}")
            model = self._download_repository.get_model(id)
            if model is None:
                log.debug(f"Adding {id} to database")
                model = self._download_repository.create_model_from_torrent(path)
            else:
                log.debug(f"{id} already in database")

            if model.status == DownloadStatus["TORRENT_FOUND"]:
                self._send_to_debrider(model, path)

            self._delete_torrent_file(path)

    def _send_to_debrider(self, download: DownloadModel, path: str):
        magnet = Torrent.get_magnet_link(path)
        debrider_id = debrider.add_magnet(magnet)
        debrider_info = debrider.get_torrent_info(debrider_id)
        download.status = DownloadStatus["TORRENT_SENT_TO_DEBRIDER"]
        self._debrider_info_repository.create_model_from_torrent_info(
            debrider_info, download
        )

    def _delete_torrent_file(self, path):
        os.remove(path)

    def __del__(self):
        self._db_session.commit()
        self._db_session.remove()


class TaskTorrentFiles(Task):
    async def run(self):
        holes_path = config.data_dir + "/holes"
        torrents = glob.glob(holes_path + "/**/*.torrent")
        for f in torrents:
            handler = TorrentFileHandler()
            handler.handle_file(f)
