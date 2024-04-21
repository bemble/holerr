from .log import Log
from . import config_models

import os
import json
import yaml

log = Log.get_logger(__name__)


class Config:
    @property
    def file_path(self) -> str:
        return os.path.abspath(self.data_dir + "/config.yaml")

    @property
    def server_dir(self) -> str:
        return os.path.abspath(os.path.dirname(__file__) + "/..")

    @property
    def public_dir(self) -> str:
        return os.path.abspath(self.server_dir + "/../public")

    @property
    def data_dir(self) -> str:
        return os.path.abspath(self.server_dir + "/../data")

    def __init__(self):
        self._conf: config_models.Config = None

        log.info("Init config...")
        conf_file = os.path.abspath(self.data_dir + "/config.yaml")
        v1_conf_file = os.path.abspath(self.data_dir + "/config.json")
        if os.path.exists(v1_conf_file):
            log.debug("Migrating v1 json configuration file...")
            self._load_v1_json(v1_conf_file)
            self.write()
            os.remove(v1_conf_file)

        if not os.path.exists(conf_file):
            raise Exception(
                "Configuration file not found, please create a config.yaml file in the data directory."
            )

    def __getattr__(self, index):
        return self._conf[index]

    def load(self):
        content = yaml.load(open(self.file_path, "r"), Loader=yaml.FullLoader)

        self._conf = config_models.Config(**content)
        if self.debug:
            Log.set_debug_regex(self.debug)

    def _load_v1_json(self, json_path: str):
        json_file = open(json_path, "r")
        content = json.load(json_file)

        if "debug" in content:
            content["debug"] = ["holerr.*"]
        if "debriders" in content:
            content["debrider"] = content["debriders"]
            del content["debriders"]
        if "downloaders" in content:
            content["downloader"] = content["downloaders"]
            del content["downloaders"]
        if "presets" in content:
            for preset in content["presets"]:
                # Convert min_file_size from bytes to human readable format
                if "min_file_size" in preset and preset["min_file_size"] is not None:
                    num = preset["min_file_size"]
                    suffix = "B"
                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                        if abs(num) < 1024.0:
                            preset["min_file_size"] = f"{num:3.1f}{unit}{suffix}"
                            break
                        num /= 1024.0

        self._conf = config_models.Config(**content)

    def _dump(self) -> str:
        return yaml.dump(
            self._conf.model_dump(),
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        ).replace(": null\n", ":\n")

    def write(self):
        str_data = self._dump()
        with open(self.file_path, "w", encoding="utf-8") as outfile:
            outfile.write(str_data)
