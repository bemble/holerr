"""Init file for workers module."""

from .worker import worker
from .task_torrent_files import TaskTorrentFiles

worker.add(TaskTorrentFiles())
