from abc import ABC, abstractmethod


class Task(ABC):
    @abstractmethod
    async def run(self):
        pass
