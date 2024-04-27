"""Init file for workers module."""

from .worker import Worker
from .tasks import download_state_transitions, torrent_files, debrider, downloader

worker = Worker()
worker.add(download_state_transitions)
worker.add(torrent_files)
worker.add(debrider)
worker.add(downloader)
