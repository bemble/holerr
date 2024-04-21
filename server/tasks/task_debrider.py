from .task import Task
from server.core.log import Log
from server.core.db import db
from server.core.config_repositories import PresetRepository
from server.database.models import DownloadModel, DownloadStatus
from server.database.repositories import (
    DownloadRepository,
    DebriderFileRepository,
    DebriderLinkRepository,
)
from server.debriders import debrider
from server.debriders.debrider_models import TorrentStatus
from server.debriders.debrider_repositories import FileRepository

log = Log.get_logger(__name__)


class DebriderDownloadHanlder:
    def set_session(self, session):
        self._db_session = session

    def handle_download(self, download: DownloadModel):
        debrider_info = debrider.get_torrent_info(download.debrider_info.id)

        if debrider_info == None:
            download.status = DownloadStatus["ERROR_DELETED_ON_DEBRIDER"]
            return

        download.debrider_info.status = debrider_info.status
        download.debrider_info.progress = debrider_info.progress

        if download.debrider_info.status == TorrentStatus["MAGNET_ERROR"]:
            log.debug("Magnet error " + download.id)
            download.status = DownloadStatus["ERROR_DEBRIDER"]

        if download.debrider_info.status == TorrentStatus["WAITING_FILES_SELECTION"]:
            log.debug("Selecting files for " + download.id)
            preset = PresetRepository.get_preset(download.preset)
            preset_files = FileRepository.get_preset_files(
                download.debrider_files, preset
            )
            files = []
            download.total_bytes = 0
            for file in preset_files:
                files.append(str(DebriderFileRepository.get_torrent_file_id(file)))
                file.selected = True
                download.total_bytes += file.bytes
            debrider.select_files(download.debrider_info.id, files)
            download.status = DownloadStatus["DEBRIDER_DOWNLOADING"]
            log.debug("Debrider is downloading " + download.id)

        if download.debrider_info.status == TorrentStatus["DOWNLOADED"]:
            log.debug("Debrider downloaded " + download.id)
            links_repo = DebriderLinkRepository()
            links_repo.set_session(self._db_session)
            links_repo.create_models_from_torrent_info(debrider_info, download)
            unrestricted_links = []
            for link in debrider_info.links:
                unrestricted_link = debrider.unrestricted_link(link)
                unrestricted_links.append(unrestricted_link)
            links_repo.create_models(unrestricted_links, True, download)
            download.status = DownloadStatus["DEBRIDER_DOWNLOADED"]

        if (
            download.debrider_info.status == TorrentStatus["COMPRESSING"]
            or download.debrider_info.status == TorrentStatus["UPLOADING"]
        ):
            log.debug("Debrider is doing post downlaod actions " + download.id)
            download.status = DownloadStatus["DEBRIDER_POST_DOWNLOAD"]

        if download.debrider_info.status == TorrentStatus["ERROR"]:
            log.debug("Debrider has torrent error " + download.id)
            download.status = DownloadStatus["ERROR_DEBRIDER"]

        if download.debrider_info.status == TorrentStatus["VIRUS"]:
            log.debug("Debrider found a virus " + download.id)
            download.status = DownloadStatus["ERROR_DEBRIDER"]

        if download.debrider_info.status == TorrentStatus["DEAD"]:
            log.debug("Debrider download is dead " + download.id)
            download.status = DownloadStatus["ERROR_DEBRIDER"]


class TaskDebrider(Task):
    async def run(self):
        self._db_session = db.new_scoped_session()
        for download in self.get_downloads():
            handler = DebriderDownloadHanlder()
            handler.set_session(self._db_session)
            handler.handle_download(download)

        self._db_session.commit()
        self._db_session.remove()

    def get_downloads(self) -> list[DownloadModel]:
        rep = DownloadRepository()
        rep.set_session(self._db_session)
        return rep.get_all_handled_by_debrider()


# func UpdateDebriderInfos(download *db.Download) {
# debrider := debriders.Get()
# if debrider == nil {
# log.Info("No debrider set")
# return
# }
#
# dbi := db.Get()
#
# previousStatus := download.Status
#
# var err error
# download.TorrentInfo, err = debrider.GetTorrentInfos(download.TorrentInfo.Id)
# if err != nil {
# log.Error(err)
# }
# if download.TorrentInfo.Status == debriderInterface.TorrentStatus["DOWNLOADED"] {
# download.Status = db.DownloadStatus["DEBRIDER_DOWNLOADED"]
# } else if download.TorrentInfo.Status == debriderInterface.TorrentStatus["ERROR"] || download.TorrentInfo.Status == debriderInterface.TorrentStatus["VIRUS"] || download.TorrentInfo.Status == debriderInterface.TorrentStatus["DEAD"] {
# download.Status = db.DownloadStatus["ERROR_DEBRIDER"]
# } else {
# download.Status = db.DownloadStatus["DEBRIDER_DOWNLOADING"]
# }
#
# if previousStatus != download.Status {
# download.StatusDetails = db.DownloadStatusDetail[download.Status]
# download.UpdatedAt = time.Now()
# }
#
# if writeErr := dbi.Write("downloads", download.Id, download); writeErr != nil {
# log.Error(writeErr)
# }
# }
