from .qbittorrent_models import Torrent, TorrentState

from holerr.database.models import Download, DownloadStatus
from holerr.core.config_repositories import PresetRepository

from datetime import datetime

class QBittorrentTorrentRepository:
    @staticmethod
    def torrent_from_download(download:Download) -> Torrent:
        time_elapsed = datetime.now().timestamp() - download.created_at.timestamp()
        time_per_percent = time_elapsed / download.total_progress
        estimated_time = (100-download.total_progress) * time_per_percent
        eta = int(round(datetime.now().timestamp() + estimated_time))
        state = TorrentState["DOWNLOADING"]
        if download.status >= DownloadStatus["ERROR_NO_FILES_FOUND"]:
            state = TorrentState["ERROR"]
        elif download.status == DownloadStatus["DOWNLOADED"]:
            state = TorrentState["UPLOADING"]

        preset = PresetRepository.get_preset(download.preset)

        return Torrent(
            hash=download.id,
            name=download.title,
            size=download.total_bytes,
            progress=download.total_progress,
            eta=eta,
            state=state,
            category=download.preset,
            save_path=preset.output_dir,
            content_path=preset.output_dir,
            ratio=1,
            last_activity=int(round(download.updated_at.timestamp())),
        )