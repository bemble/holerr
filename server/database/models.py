from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

TABLE_DOWNLOAD = "download"
TABLE_DEBRIDER_INFO = "debrider_info"
TABLE_DEBRIDER_FILE = "debrider_file"
TABLE_DEBRIDER_LINK = "debrider_link"
TABLE_DOWNLOADER_INFO = "downloader_info"
TABLE_DOWNLOADER_TASK = "downloader_task"

DownloadStatus = {
    "TORRENT_FOUND": 0,
    "TORRENT_SENT_TO_DEBRIDER": 1,
    "DEBRIDER_DOWNLOADING": 2,
    "DEBRIDER_DOWNLOADED": 3,
    "SENT_TO_DOWNLOADER": 4,
    "DOWNLOADER_DOWNLOADING": 5,
    "DOWNLOADER_DOWNLOADED": 6,
    "ERROR_NO_FILES_FOUND": 100,
    "ERROR_DEBRIDER": 101,
    "ERROR_DOWNLOADER": 102,
}

DownloadStatusDetail = {
    DownloadStatus["TORRENT_FOUND"]: "Torrent file found on drive",
    DownloadStatus["TORRENT_SENT_TO_DEBRIDER"]: "Torrent sent to debrider for download",
    DownloadStatus[
        "DEBRIDER_DOWNLOADING"
    ]: "Debrider is downloading files, check on debrider",
    DownloadStatus["DEBRIDER_DOWNLOADED"]: "Debrider download is terminated",
    DownloadStatus["SENT_TO_DOWNLOADER"]: "Debrided files sent to downloader",
    DownloadStatus["DOWNLOADER_DOWNLOADING"]: "Downloader is downloading the files",
    DownloadStatus["DOWNLOADER_DOWNLOADED"]: "Downloader task is terminated",
    DownloadStatus["ERROR_NO_FILES_FOUND"]: "No files found",
    DownloadStatus["ERROR_DEBRIDER"]: "Debrider error",
    DownloadStatus["ERROR_DOWNLOADER"]: "Downloader error",
}


class Base(DeclarativeBase):
    pass


class DownloadModel(Base):
    __tablename__ = TABLE_DOWNLOAD

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    preset: Mapped[str]
    status: Mapped[int]
    total_bytes: Mapped[int]

    debrider_info: Mapped["DebriderInfoModel"] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )
    debrider_files: Mapped[List["DebriderFileModel"]] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )
    debrider_links: Mapped[List["DebriderLinkModel"]] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )
    downloader_info: Mapped["DownloaderInfoModel"] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )
    downloader_tasks: Mapped[List["DownloaderTaskModel"]] = relationship(
        back_populates="download", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"DownloadModel(id={self.id}, title={self.title}, status={self.status})"


class DebriderInfoModel(Base):
    __tablename__ = TABLE_DEBRIDER_INFO

    id: Mapped[str] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    filename: Mapped[str]
    bytes: Mapped[int]
    progress: Mapped[int]
    status: Mapped[str]

    download: Mapped["DownloadModel"] = relationship(back_populates="debrider_info")


class DebriderFileModel(Base):
    __tablename__ = TABLE_DEBRIDER_FILE

    id: Mapped[int] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    path: Mapped[str]
    bytes: Mapped[int]
    selected: Mapped[int]

    download: Mapped["DownloadModel"] = relationship(back_populates="debrider_files")


class DebriderLinkModel(Base):
    __tablename__ = TABLE_DEBRIDER_LINK

    link: Mapped[str] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    is_unrestricted: Mapped[bool]

    download: Mapped["DownloadModel"] = relationship(back_populates="debrider_links")


class DownloaderInfoModel(Base):
    __tablename__ = TABLE_DOWNLOADER_INFO

    id: Mapped[str] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    progress: Mapped[int]

    download: Mapped["DownloadModel"] = relationship(back_populates="downloader_info")


class DownloaderTaskModel(Base):
    __tablename__ = TABLE_DOWNLOADER_TASK

    id: Mapped[str] = mapped_column(primary_key=True)
    download_id: Mapped[int] = mapped_column(ForeignKey(TABLE_DOWNLOAD + ".id"))
    status: Mapped[int]
    bytes_downloaded: Mapped[int]

    download: Mapped["DownloadModel"] = relationship(back_populates="downloader_tasks")
