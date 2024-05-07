from . import config
from .log import Log
from .config_models import Preset
from .exceptions import NotFoundException, AlreadyExistsException

import os

log = Log.get_logger(__name__)


class PresetRepository:
    @staticmethod
    def get_watch_directory(preset: Preset) -> str:
        return config.data_dir + "/" + preset.watch_dir

    @staticmethod
    def create_watch_directory(preset: Preset):
        path = PresetRepository.get_watch_directory(preset)
        if not os.path.exists(path):
            os.makedirs(path)
            log.debug(f"Created directory {path}")
        else:
            log.debug(f"Preset directory {path} already exists, skipping...")

    @staticmethod
    def create_watch_directories():
        for preset in config.presets:
            PresetRepository.create_watch_directory(preset)

    @staticmethod
    def delete_watch_directory(preset: Preset):
        path = PresetRepository.get_watch_directory(preset)
        if os.path.exists(path):
            os.rmdir(path)

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

    @staticmethod
    def add_preset(preset: Preset) -> Preset:
        p = PresetRepository.get_preset(preset.name)
        if p is not None:
            raise AlreadyExistsException(f"Preset {preset.name} already exists")
        config.presets.append(preset)
        PresetRepository.create_watch_directory(preset)
        config.write()
        return preset

    @staticmethod
    def update_preset(preset_name: str, update_data: dict) -> Preset:
        preset = PresetRepository.get_preset(preset_name)
        if preset is None:
            raise NotFoundException(f"Preset {preset_name} not found")
        update_watch_dir = "watch_dir" in update_data
        if update_watch_dir:
            PresetRepository.delete_watch_directory(preset)
        preset.update(update_data)
        config.write()
        if update_watch_dir:
            PresetRepository.create_watch_directory(preset)
        return preset

    @staticmethod
    def delete_preset(name: str):
        for index, preset in enumerate(config.presets):
            if preset.name == name:
                PresetRepository.delete_watch_directory(preset)
                config.presets.pop(index)
                config.write()
                return
        raise NotFoundException(f"Preset {name} not found")
