"""Init file for workers module."""

from .worker import Worker
from .task_torrent_files import TaskTorrentFiles
from .task_debrider import TaskDebrider

worker = Worker()
worker.add(TaskTorrentFiles())
worker.add(TaskDebrider())
