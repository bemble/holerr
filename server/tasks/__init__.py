"""Init file for workers module."""

from .worker import Worker
from .task_download_state_transitions import TaskDownloadStateTransition
from .task_torrent_files import TaskTorrentFiles
from .task_debrider import TaskDebrider
from .task_downloader import TaskDownloader

worker = Worker()
worker.add(TaskDownloadStateTransition())
worker.add(TaskTorrentFiles())
worker.add(TaskDebrider())
worker.add(TaskDownloader())
