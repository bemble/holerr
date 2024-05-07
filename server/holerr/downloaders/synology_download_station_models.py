from typing import Optional, Any
from pydantic import BaseModel


class Error(BaseModel):
    code: int


class Status(BaseModel):
    error: Optional[Error] = None
    success: bool


class AuthData(BaseModel):
    sid: str
    did: str


class Auth(Status):
    data: Optional[AuthData] = None


class TaskDetail(BaseModel):
    completed_time: int
    connected_leechers: int
    connected_peers: int
    connected_seeders: int
    create_time: int
    destination: str
    seedelapsed: int
    started_time: int
    total_peers: int
    total_pieces: int
    unzip_password: str
    uri: str
    waiting_seconds: int


class TaskTransfer(BaseModel):
    downloaded_pieces: int
    size_downloaded: int
    size_uploaded: int
    speed_download: int
    speed_upload: int


class TaskAdditional(BaseModel):
    detail: Optional[TaskDetail] = None
    transfer: Optional[TaskTransfer] = None
    file: Optional[list[Any]] = None  # BT only
    tracker: Optional[Any] = None  # BT only
    peer: Optional[Any] = None  # BT only


class Task(BaseModel):
    id: str
    type: str
    username: str
    title: str
    size: int
    status: str
    additional: TaskAdditional


class TasksData(BaseModel):
    total: Optional[int] = None
    offset: Optional[int] = None
    tasks: list[Task]


class Tasks(Status):
    data: Optional[TasksData] = None
