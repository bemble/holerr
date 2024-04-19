# watch file change, new torrent file, new magnet link

# run periodicall updates

from core.config import config
from .log import log

import asyncio
import threading
import glob


class Handler:
    workers: dict[str, threading.Thread] = {}

    def start(self):
        self.stop()

        self.workers["updates"] = threading.Thread(target=self.run_updates_worker)
        self.workers["updates"] = threading.Thread(target=self.run_torrent_files_worker)

        log.info("Starting workers...")
        for name in self.workers.keys():
            log.debug(f"Starting {name} worker...")
            self.workers[name].start()

    def stop(self):
        for name in self.workers.keys():
            log.debug(f"Stopping {name} worker...")
            self.workers[name].join()
            del self.workers[name]

    def run_updates_worker(self):
        asyncio.run(self._updates_worker())

    def run_torrent_files_worker(self):
        asyncio.run(self._torrent_files_worker())

    async def _updates_worker(self):
        log.debug("Updates worker started")
        while True:
            # for each download in db, check updates
            await asyncio.sleep(5)

    async def _torrent_files_worker(self):
        log.debug("Torrent files worker started")
        holes_path = config.data_dir + "/holes"
        while True:
            torrents = glob.glob(holes_path + "/**/*.torrent")
            for f in torrents:
                # add new torrents
                pass
            await asyncio.sleep(5)


handler = Handler()
