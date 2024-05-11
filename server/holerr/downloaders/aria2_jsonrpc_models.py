from typing import Optional, Any
from pydantic import BaseModel


class Aria2Base(BaseModel):
    id: str
    jsonrpc: str

class StatusResult(BaseModel):
    downloadSpeed: str
    numActive: str
    numStopped: str
    numStoppedTotal: str
    numWaiting: str
    uploadSpeed: str

class Status(Aria2Base):
    result: StatusResult