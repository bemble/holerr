from holerr.core.log import Log
from .task import Task

import asyncio
import threading
from datetime import datetime

log = Log.get_logger(__name__)


class Worker:
    _worker: threading.Thread = None
    _tasks: list[Task] = []
    last_run: datetime = None

    def add(self, task: Task):
        log.debug(type(task).__name__ + " added")
        self._tasks.append(task)

    def start(self):
        self.stop()

        self._worker = threading.Thread(target=self.run)

        self._worker.start()

    def stop(self):
        if self._worker:
            log.debug("Stopping worker")
            self._worker.join()
            del self._worker

    def run(self):
        asyncio.run(self._run())

    async def _run(self):
        log.debug("Starting workers")
        while True:
            for task in self._tasks:
                try:
                    await task.run()
                except Exception as e:
                    log.error(f"Error while running task, {e}")
                self.last_run = datetime.now()
            await asyncio.sleep(5)
