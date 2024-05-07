from holerr.core.config_models import Preset
from .debrider_models import File


class FileRepository:
    @staticmethod
    def get_preset_files(files: list[File], preset: Preset) -> list[File]:
        filtered_files = []
        for file in files:
            if not (
                preset.min_file_size_byte == 0
                or file.bytes >= preset.min_file_size_byte
            ):
                continue
            file_extention = file.path.split(".")[-1]
            if not (
                preset.file_extensions is None
                or file_extention in preset.file_extensions
            ):
                continue
            filtered_files.append(file)
        return filtered_files
