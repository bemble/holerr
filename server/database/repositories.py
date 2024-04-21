from abc import ABC, abstractmethod

from .models import Base, DownloadModel, DownloadStatus, DebriderInfoModel
from server.util.torrent import Torrent
from server.core.config_repositories import PresetRepository
from server.debriders.debrider_models import TorrentInfo

import os
from sqlalchemy import select


class Repository(ABC):
    def set_session(self, session):
        self.session = session
        pass

    @abstractmethod
    def get_model(self, id: any) -> Base | None:
        pass

    @abstractmethod
    def create_model(self, **kwargs) -> Base:
        pass


class DownloadRepository(Repository):
    @staticmethod
    def compute_id_from_torrent(path: str) -> str:
        return Torrent.get_infohash(path)

    @staticmethod
    def get_name_from_torrent(path: str) -> str:
        return Torrent.get_name(path)

    def get_model(self, id: str) -> DownloadModel | None:
        res = self.session.scalars(select(DownloadModel).where(DownloadModel.id == id))
        return res.one_or_none()

    def create_model(self, **kwargs) -> DownloadModel:
        model = DownloadModel(**kwargs)
        self.session.add(model)
        self.session.commit()
        return model

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
            title=title,
            status=status,
            preset=preset.name,
            total_bytes=total_bytes,
        )


class DebriderInfoRepository(Repository):
    def create_model(self, **kwargs) -> DebriderInfoModel:
        model = DebriderInfoModel(**kwargs)
        self.session.add(model)
        self.session.commit()
        return model

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

    def get_model(self, id: str) -> DebriderInfoModel | None:
        res = self.session.scalars(
            select(DebriderInfoModel).where(DebriderInfoModel.id == id)
        )
        return res.one_or_none()
