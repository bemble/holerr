from typing import Optional
from pydantic import BaseModel, model_validator, ValidationError

import re


class Preset(BaseModel):
    name: str
    watch_dir: str
    output_dir: str
    create_sub_dir: Optional[bool] = None
    file_extensions: Optional[list[str]] = None
    min_file_size: Optional[str] = None

    @property
    def min_file_size_byte(self) -> int:
        if not self.min_file_size:
            return 0

        units = {"B": 1, "KB": 2**10, "MB": 2**20, "GB": 2**30, "TB": 2**40}
        size = self.min_file_size
        if not re.match(r" ", size):
            size = re.sub(r"([KMGT]?B)", r" \1", size)
        number, unit = [string.strip() for string in size.split()]
        return int(float(number) * units[unit])


class RealDebrid(BaseModel):
    api_key: str


class Debrider(BaseModel):
    real_debrid: Optional[RealDebrid] = None

    @model_validator(mode="after")
    def verify_any_of(self):
        if not self.real_debrid:
            raise ValidationError("A debrider needs to be set.")
        return self


class SynologyDownloadStation(BaseModel):
    endpoint: str
    username: str
    password: str


class Downloader(BaseModel):
    synology_download_station: Optional[SynologyDownloadStation] = None

    @model_validator(mode="after")
    def verify_any_of(self):
        if not self.synology_download_station:
            raise ValidationError("A downloader needs to be set.")
        return self


class Config(BaseModel):
    debug: Optional[list[str]] = None
    api_key: Optional[str] = None
    base_path: Optional[str] = None
    debrider: Debrider = None
    downloader: Downloader = None
    presets: Optional[list[Preset]] = None

    def __getitem__(self, index):
        return getattr(self, index)
