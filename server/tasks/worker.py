from core.log import Log
from .task import Task

import asyncio
import threading

log = Log.get_logger(__name__)


class Worker:
    _worker: threading.Thread = None
    _tasks: list[Task] = []

    def add(self, task: Task):
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
                await task.run()
            await asyncio.sleep(5)


worker = Worker()
