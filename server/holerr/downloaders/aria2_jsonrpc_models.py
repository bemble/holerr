from typing import Optional, Any
from pydantic import BaseModel

Aria2TaskStatus = {
    "WAITING": "waiting",
    "ACTIVE": "active",
    "PAUSED": "paused",
    "COMPLETE": "complete",
    "REMOVED": "removed",
    "ERROR": "error",
}

class Aria2Base(BaseModel):
    id: str
    jsonrpc: str

class GlobalStatusResult(BaseModel):
    downloadSpeed: str
    numActive: str
    numStopped: str
    numStoppedTotal: str
    numWaiting: str
    uploadSpeed: str

class GlobalStatus(Aria2Base):
    result: GlobalStatusResult


class File(BaseModel):
    completedLength: str
    index: str
    length: str
    path: str
    selected: str
    uris: list[Any]

class TaskStatusResult(BaseModel):
    bitfield: str
    completedLength: str
    connections: str
    dir: str
    downloadSpeed: str
    files: list[File]
    gid: str
    numPieces: str
    pieceLength: str
    status: str
    totalLength: str
    uploadLength: str
    uploadSpeed: str

class TaskStatus(Aria2Base):
    result: TaskStatusResult

class AddUriResult(BaseModel):
    result: str