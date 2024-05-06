from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func
from datetime import datetime

TABLE_DOWNLOAD = "download"
TABLE_DEBRIDER_INFO = "debrider_info"
TABLE_DEBRIDER_FILE = "debrider_file"
TABLE_DEBRIDER_LINK = "debrider_link"
TABLE_DOWNLOADER_INFO = "downloader_info"
TABLE_DOWNLOADER_TASK = "downloader_task"

DownloadStatus = {
    "TORRENT_FOUND": 0,
    "TORRENT_SENT_TO_DEBRIDER": 10,
    "DEBRIDER_DOWNLOADING": 11,
    "DEBRIDER_POST_DOWNLOAD": 12,
    "DEBRIDER_DOWNLOADED": 13,
    "SENT_TO_DOWNLOADER": 20,
    "DOWNLOADER_DOWNLOADING": 21,
    "DOWNLOADER_DOWNLOADED": 22,
    "DOWNLOADED": 30,
    "ERROR_NO_FILES_FOUND": 100,
    "ERROR_DEBRIDER": 101,
    "ERROR_DOWNLOADER": 102,
    "ERROR_DELETED_ON_DEBRIDER": 103,
}


class Base(DeclarativeBase):
    pass


class Download(Base):
    __tablename__ = TABLE_DOWNLOAD

    id: Mapped[str] = mapped_column(primary_key=True)
    magnet: Mapped[str]
    title: Mapped[str]
    preset: Mapped[str]
    status: Mapped[int]
    total_bytes: Mapped[int]
    total_progress: Mapped[int]
    to_delete: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    debrider_info: Mapped["DebriderInfo"] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )
    debrider_files: Mapped[List["DebriderFile"]] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )
    debrider_links: Mapped[List["DebriderLink"]] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )
    downloader_info: Mapped["DownloaderInfo"] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )
    downloader_tasks: Mapped[List["DownloaderTask"]] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"DownloadModel(id={self.id}, title={self.title}, status={self.status})"


class DebriderInfo(Base):
    __tablename__ = TABLE_DEBRIDER_INFO

    id: Mapped[str] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    filename: Mapped[str]
    bytes: Mapped[int]
    progress: Mapped[int]
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    download: Mapped["Download"] = relationship(back_populates="debrider_info")


class DebriderFile(Base):
    __tablename__ = TABLE_DEBRIDER_FILE

    id: Mapped[str] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    path: Mapped[str]
    bytes: Mapped[int]
    selected: Mapped[int]

    download: Mapped["Download"] = relationship(back_populates="debrider_files")


class DebriderLink(Base):
    __tablename__ = TABLE_DEBRIDER_LINK

    link: Mapped[str] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    is_unrestricted: Mapped[bool]

    download: Mapped["Download"] = relationship(back_populates="debrider_links")


class DownloaderInfo(Base):
    __tablename__ = TABLE_DOWNLOADER_INFO

    download_id: Mapped[int] = mapped_column(
        ForeignKey(TABLE_DOWNLOAD + ".id"), primary_key=True
    )
    progress: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    download: Mapped["Download"] = relationship(back_populates="downloader_info")


class DownloaderTask(Base):
    __tablename__ = TABLE_DOWNLOADER_TASK

    id: Mapped[str] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    status: Mapped[int]
    bytes_downloaded: Mapped[int]

    download: Mapped["Download"] = relationship(back_populates="downloader_tasks")
