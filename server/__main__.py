from core.config import config
from tasks.worker import worker
from tasks.task_torrent_files import TaskTorrentFiles

import sys


def _init():
    config.load()
    worker.add(TaskTorrentFiles())


def main() -> int:
    worker.start()
    return 0


if __name__ == "__main__":
    _init()
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        worker.stop()
