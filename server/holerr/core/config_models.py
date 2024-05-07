from .log import Log
from holerr.utils import secrets

from typing import Optional
from pydantic import (
    SecretStr,
    BaseModel,
    model_validator,
    ValidationError,
    field_serializer,
)

import re

log = Log.get_logger(__name__)


class Model(BaseModel):
    def update(self, data: dict):
        cur_update = {}
        for k, v in data.items():
            if isinstance(v, dict):
                log.debug(f"updating {k} is dict, {v}")
                getattr(self, k).update(v)
            else:
                cur_update[k] = v

        # validate
        self.model_copy(update=cur_update)
        for k, v in cur_update.items():
            if isinstance(v, list):
                cur = getattr(self, k)
                if not isinstance(cur, list):
                    setattr(self, k, [])
                else:
                    getattr(self, k).clear()
                for item in v:
                    getattr(self, k).append(item)
            else:
                setattr(self, k, v)

    def _dump_secret(self, v, info):
        value = v.get_secret_value()
        if info.mode == "python":
            return value
        return secrets.hide(value)


class Preset(Model):
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


class RealDebrid(Model):
    api_key: SecretStr

    @field_serializer("api_key")
    def dump_secret(self, v, info):
        return self._dump_secret(v, info)


class Debrider(Model):
    real_debrid: Optional[RealDebrid] = None

    @model_validator(mode="after")
    def verify_any_of(self):
        if not self.real_debrid:
            raise ValidationError("A debrider needs to be set.")
        return self


class SynologyDownloadStation(Model):
    endpoint: str
    username: str
    password: SecretStr

    @field_serializer("password")
    def dump_secret(self, v, info):
        return self._dump_secret(v, info)


class Downloader(Model):
    synology_download_station: Optional[SynologyDownloadStation] = None

    @model_validator(mode="after")
    def verify_any_of(self):
        if not self.synology_download_station:
            raise ValidationError("A downloader needs to be set.")
        return self


class Config(Model):
    debug: Optional[list[str]] = None
    api_key: Optional[SecretStr] = None
    base_path: Optional[str] = None
    debrider: Debrider = None
    downloader: Downloader = None
    presets: Optional[list[Preset]] = None

    @field_serializer("api_key")
    def dump_secret(self, v, info):
        return self._dump_secret(v, info)

    def __getitem__(self, index):
        return getattr(self, index)
