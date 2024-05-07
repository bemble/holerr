"""Init file for workers module."""

from .worker import Worker
from .tasks import (
    delete_downloads,
    download_state_transitions,
    torrent_files,
    debrider,
    downloader,
)

worker = Worker()
worker.add(delete_downloads)
worker.add(download_state_transitions)
worker.add(torrent_files)
worker.add(debrider)
worker.add(downloader)
