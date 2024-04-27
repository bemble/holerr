from .models import (
    Base,
    DownloadModel,
    DownloadStatus,
    DebriderInfoModel,
    DebriderFileModel,
    DebriderLinkModel,
    DownloaderInfoModel,
    DownloaderTaskModel,
)
from server.utils import torrent
from server.core.config_repositories import PresetRepository
from server.debriders.debrider_models import TorrentInfo

import os
from sqlalchemy import select
from sqlalchemy.orm import Session


class Repository:
    def __init__(self, session: Session, entity: Base):
        self.session = session
        self.entity = entity

    def get_model(self, id: any) -> Base | None:
        res = self.session.scalars(select(self.entity).where(self.entity.id == id))
        return res.one_or_none()

    def get_all_models(self, conditions=True) -> list[Base]:
        res = self.session.scalars(select(self.entity).where(conditions))
        return res.all()

    def create_model(self, **kwargs) -> Base:
        model = self.entity(**kwargs)
        self.session.add(model)
        self.session.commit()
        return model


class DownloadRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DownloadModel)

    @staticmethod
    def compute_id_from_torrent(path: str) -> str:
        return torrent.get_hash(path)

    @staticmethod
    def get_name_from_torrent(path: str) -> str:
        return torrent.get_name(path)

    def create_model_from_torrent(self, path: str) -> DownloadModel:
        id = DownloadRepository.compute_id_from_torrent(path)
        title = DownloadRepository.get_name_from_torrent(path)
        status = DownloadStatus["TORRENT_FOUND"]
        preset = PresetRepository.get_preset_by_folder(os.path.dirname(path))
        total_bytes = 0
        if preset is None:
            raise Exception("Preset not found for {path}")
        return self.create_model(
            id=id,
            magnet=torrent.get_magnet_link(path),
            title=title,
            status=status,
            preset=preset.name,
            total_bytes=total_bytes,
        )

    def get_all_handled_by_debrider(self) -> list[DownloadModel]:
        return self.get_all_models(
            DownloadModel.status.in_(
                tuple(
                    [
                        DownloadStatus["TORRENT_SENT_TO_DEBRIDER"],
                        DownloadStatus["DEBRIDER_DOWNLOADING"],
                        DownloadStatus["DEBRIDER_POST_DOWNLOAD"],
                    ]
                )
            )
        )

    def get_all_handled_by_download_state_transition(self) -> list[DownloadModel]:
        return self.get_all_models(
            DownloadModel.status.in_(
                tuple(
                    [
                        DownloadStatus["TORRENT_FOUND"],
                        DownloadStatus["DEBRIDER_DOWNLOADED"],
                    ]
                )
            )
        )

    def get_all_handled_by_downloader(self) -> list[DownloadModel]:
        return self.get_all_models(
            DownloadModel.status.in_(
                tuple(
                    [
                        DownloadStatus["SENT_TO_DOWNLOADER"],
                        DownloadStatus["DOWNLOADER_DOWNLOADING"],
                    ]
                )
            )
        )


class DebriderInfoRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DebriderInfoModel)

    def create_model_from_torrent_info(
        self, torrent_info: TorrentInfo, download: DownloadModel
    ) -> DebriderInfoModel:
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
        super().__init__(session, DebriderFileModel)

    def create_models_from_torrent_info(
        self, torrent_info: TorrentInfo, download: DownloadModel
    ) -> list[DebriderFileModel]:
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
    def get_torrent_file_id(model: DebriderFileModel) -> int:
        return int(model.id.split(".")[-1])


class DebriderLinkRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DebriderLinkModel)

    def create_models_from_torrent_info(
        self, torrent_info: TorrentInfo, download: DownloadModel
    ) -> list[DebriderLinkModel]:
        links = []
        for link in torrent_info.links:
            links.append(link)
        return self.create_models(links, False, download)

    def create_models(
        self, in_links: list[str], is_unrestricted: bool, download: DownloadModel
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
        super().__init__(session, DownloaderInfoModel)


class DownloaderTaskRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(session, DownloaderTaskModel)
