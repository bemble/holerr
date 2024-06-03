from .models import (
    Base,
    Download,
    DownloadStatus,
    DebriderInfo,
    DebriderFile,
    DebriderLink,
    DownloaderInfo,
    DownloaderTask,
)
from holerr.utils import torrent, magnet
from holerr.core.config_repositories import PresetRepository
from holerr.debriders.debrider_models import TorrentInfo
from holerr.core.exceptions import NotFoundException, AlreadyExistsException

import os
from sqlalchemy import select
from sqlalchemy.orm import Session


class Repository:
    def __init__(self, session: Session, entity: Base):
        self.session = session
        self.entity = entity

    def get_model(self, id: any) -> Base | None:
        res = self.get_all_models(self.entity.id == id)
        return res[0] if len(res) > 0 else None

    def get_all_models(self, conditions=True, options=None) -> list[Base]:
        query = select(self.entity).where(conditions)
        if options:
            query = query.options(options)
        res = self.session.scalars(query)
        return res.all()

    def create_model(self, **kwargs) -> Base:
        model = self.entity(**kwargs)
        self.session.add(model)
        self.session.commit()
        return model


class DownloadRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, Download)

    @staticmethod
    def compute_id_from_torrent(path: str) -> str:
        return torrent.get_hash(path)

    @staticmethod
    def get_name_from_torrent(path: str) -> str:
        return torrent.get_name(path)

    def create_model_from_torrent(self, path: str) -> Download:
        id = DownloadRepository.compute_id_from_torrent(path)
        if self.get_model(id) is not None:
            raise AlreadyExistsException(f"Download {id} already exists")
        title = DownloadRepository.get_name_from_torrent(path)
        status = DownloadStatus["TORRENT_FOUND"]
        preset = PresetRepository.get_preset_by_folder(os.path.dirname(path))
        if preset is None:
            raise NotFoundException("Preset not found for {path}")
        return self.create_model(
            id=id,
            magnet=torrent.get_magnet_link(path),
            title=title,
            status=status,
            preset=preset.name,
            total_bytes=0,
            total_progress=0,
        )

    def create_model_from_magnet(self, magnet_uri: str, preset_name: str) -> Download:
        id = magnet.get_hash(magnet_uri)
        if self.get_model(id) is not None:
            raise AlreadyExistsException(f"Download {id} already exists")
        title = magnet.get_name(magnet_uri)
        status = DownloadStatus["TORRENT_FOUND"]
        preset = PresetRepository.get_preset(preset_name)
        if preset is None:
            raise NotFoundException(f"Preset {preset_name} not found")
        return self.create_model(
            id=id,
            magnet=magnet_uri,
            title=title,
            status=status,
            preset=preset.name,
            total_bytes=0,
            total_progress=0,
        )

    def get_all_handled_by_debrider(self) -> list[Download]:
        return self.get_all_models(
            Download.status.in_(
                tuple(
                    [
                        DownloadStatus["TORRENT_SENT_TO_DEBRIDER"],
                        DownloadStatus["DEBRIDER_DOWNLOADING"],
                        DownloadStatus["DEBRIDER_POST_DOWNLOAD"],
                    ]
                )
            ),
            not Download.to_delete,
        )

    def get_all_handled_by_download_state_transition(self) -> list[Download]:
        return self.get_all_models(
            Download.status.in_(
                tuple(
                    [
                        DownloadStatus["TORRENT_FOUND"],
                        DownloadStatus["DEBRIDER_DOWNLOADED"],
                    ]
                )
            ),
            not Download.to_delete,
        )

    def get_all_handled_by_downloader(self) -> list[Download]:
        return self.get_all_models(
            Download.status.in_(
                tuple(
                    [
                        DownloadStatus["SENT_TO_DOWNLOADER"],
                        DownloadStatus["DOWNLOADER_DOWNLOADING"],
                    ]
                )
            ),
            not Download.to_delete,
        )

    def get_all_to_delete(self) -> list[Download]:
        return self.get_all_models(
            Download.to_delete,
        )

    def get_all_for_preset(self, preset_name: str) -> list[Download]:
        return self.get_all_models(Download.preset == preset_name)

    def clean_downloaded(self) -> list[str]:
        deleted_ids = []
        downloads = self.get_all_models(Download.status == DownloadStatus["DOWNLOADED"])
        for download in downloads:
            deleted_ids.append(download.id)
            self.session.delete(download)
        self.session.commit()
        return deleted_ids

    def delete_download(self, id: str):
        download = self.get_model(id)
        if download is None:
            raise NotFoundException(f"Download {id} not found")
        if download.status == DownloadStatus["TORRENT_FOUND"]:
            raise Exception(f"Cannot delete download {id}, download is not started")

        if (
            download.status >= DownloadStatus["TORRENT_SENT_TO_DEBRIDER"]
            and download.status < DownloadStatus["DEBRIDER_DOWNLOADED"]
        ):
            # Debrider is working on it, we can't delete it
            raise Exception(f"Download {id} is being processed by the debrider")


class DebriderInfoRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DebriderInfo)

    def create_model_from_torrent_info(
        self, torrent_info: TorrentInfo, download: Download
    ) -> DebriderInfo:
        return self.create_model(
            id=torrent_info.id,
            download=download,
            filename=torrent_info.filename,
            bytes=torrent_info.bytes,
            progress=torrent_info.progress,
            status=torrent_info.status,
        )


class DebriderFileRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DebriderFile)

    def create_models_from_torrent_info(
        self, torrent_info: TorrentInfo, download: Download
    ) -> list[DebriderFile]:
        files = []
        for torrent_file in torrent_info.files:
            files.append(
                self.create_model(
                    id=DebriderFileRepository.compute_id(torrent_info, torrent_file.id),
                    download=download,
                    path=torrent_file.path,
                    bytes=torrent_file.bytes,
                    selected=torrent_file.selected,
                )
            )

    @staticmethod
    def compute_id(torrent_info: TorrentInfo, file_id: int) -> str:
        return torrent_info.id + "." + str(file_id)

    @staticmethod
    def get_torrent_file_id(model: DebriderFile) -> int:
        return int(model.id.split(".")[-1])


class DebriderLinkRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DebriderLink)

    def create_models_from_torrent_info(
        self, torrent_info: TorrentInfo, download: Download
    ) -> list[DebriderLink]:
        links = []
        for link in torrent_info.links:
            links.append(link)
        return self.create_models(links, False, download)

    def create_models(
        self, in_links: list[str], is_unrestricted: bool, download: Download
    ):
        links = []
        for link in in_links:
            links.append(
                self.create_model(
                    link=link,
                    download=download,
                    is_unrestricted=is_unrestricted,
                )
            )
        return links


class DownloaderInfoRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DownloaderInfo)


class DownloaderTaskRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DownloaderTask)
