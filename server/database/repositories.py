from .models import DownloadModel, DownloadStatus
from .db import db
from server.util.torrent import Torrent
from server.core.config_repositories import PresetRepository

import os
from sqlalchemy import select


class DownloadRepository:
    @staticmethod
    def compute_id_from_torrent(path: str) -> str:
        return Torrent.get_infohash(path)

    @staticmethod
    def get_name_from_torrent(path: str) -> str:
        return Torrent.get_name(path)
        # return str(subj[b"name"], "utf-8")

    @staticmethod
    def get_model(id: str) -> DownloadModel | None:
        session = db.new_session()
        res = session.execute(select(DownloadModel).where(DownloadModel.id == id))
        return res.one_or_none()

    @staticmethod
    def create_model(**kwargs) -> DownloadModel:
        session = db.new_scoped_session()
        model = DownloadModel(**kwargs)
        session.add(model)
        session.commit()
        session.remove()
        return model

    @staticmethod
    def create_model_from_torrent(path: str) -> DownloadModel:
        id = DownloadRepository.compute_id_from_torrent(path)
        title = DownloadRepository.get_name_from_torrent(path)
        status = DownloadStatus["TORRENT_FOUND"]
        preset = PresetRepository.get_preset_by_folder(os.path.dirname(path))
        total_bytes = 0
        if preset is None:
            raise Exception("Preset not found for {path}")
        return DownloadRepository.create_model(
            id=id,
            title=title,
            status=status,
            preset=preset.name,
            total_bytes=total_bytes,
        )
