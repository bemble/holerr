from .config import config
from .log import Log
from .config_models import Preset

import os

log = Log.get_logger(__name__)


class PresetRepository:
    @staticmethod
    def create_directories():
        data_dir = config.data_dir
        for preset in config.presets:
            path = data_dir + "/" + preset.watch_dir
            if not os.path.exists(path):
                os.makedirs(path)
                log.debug(f"Created directory {path}")
            else:
                log.debug(f"Preset directory {path} already exists, skipping...")

    @staticmethod
    def get_preset(name: str) -> Preset | None:
        for preset in config.presets:
            if preset.name == name:
                return preset
        return None

    @staticmethod
    def get_preset_by_folder(folder: str) -> Preset | None:
        data_dir = config.data_dir
        for preset in config.presets:
            if data_dir + "/" + preset.watch_dir == folder:
                return preset
        return None
