from .downloader import Downloader
from holerr.core import config
from holerr.core.log import Log
from .aria2_jsonrpc_models import Aria2TaskStatus, GlobalStatus, GlobalStatusResult, TaskStatus, AddUriResult
from .downloader_models import DownloadStatus
from holerr.core.config_models import Preset
from holerr.core.exceptions import HttpRequestException

from typing import Any
import requests
import json
import uuid

log = Log.get_logger(__name__)


class Aria2JsonRpc(Downloader):
    def get_id(self) -> str:
        return "aria2_jsonrpc"

    def get_name(self) -> str:
        return "Aria2 JSON-RPC"

    def is_connected(self) -> bool:
        try:
            self._get_global_status()
        except Exception:
            return False
        return True

    def add_download(self, uri: str, title: str, preset: Preset) -> str:
        payload = {
            "method": "aria2.addUri",
            "params": [[uri]]
        }

        if preset.output_dir is not None:
            destination = preset.output_dir
            if preset.create_sub_dir:
                destination += "/" + Downloader.get_sub_folder_name(title)

            payload["params"].append({"dir": destination})

        res = self._call(payload)
        if res.status_code != 200:
            raise HttpRequestException("Could not add download " + res, res.status_code)
        return AddUriResult(**res.json()).result

    def get_task_status(self, id: str) -> tuple[str, int]:
        payload = {
            "method": "aria2.tellStatus",
            "params": [id]
        }
        res = self._call(payload)
        if res.status_code != 200:
            raise HttpRequestException("Error while getting task status", res.status_code)
        status_data = TaskStatus(**res.json()).result
        return status_data.status, int(status_data.completedLength)


    def delete_download(self, id: str):
        payload = {
            "method": "aria2.forceRemove",
            "params": [id]
        }
        res = self._call(payload)
        if res.status_code != 200:
            log.debug(res)
            raise HttpRequestException(f"Could not delete download {id}", res.status_code)

    def _call(self, payload:dict[str, Any]):
        aria2_cfg = config.downloader.aria2_jsonrpc

        headers = {
            "Content-Type": "application/json",
        }

        if aria2_cfg.secret is not None:
            if "params" not in payload:
                payload["params"] = []
            payload["params"].insert(0, f"token:{aria2_cfg.secret.get_secret_value()}")

        if "id" not in payload:
            payload["id"] = Aria2JsonRpc.compute_call_id()
        if "jsonrpc" not in payload:
            payload["jsonrpc"] = "2.0"

        data = json.dumps(payload)
        return requests.request("POST", config.downloader.aria2_jsonrpc.endpoint, headers=headers, data=data)

    def _get_global_status(self) -> GlobalStatusResult:
        payload = {
            "method": "aria2.getGlobalStat",
        }
        res = self._call(payload)
        if res.status_code != 200:
            raise HttpRequestException("Error while getting global status", res.status_code)
        return GlobalStatus(**res.json()).result

    @staticmethod
    def compute_call_id() -> str:
        return f"holerr.{str(uuid.uuid4())}"

    def to_download_status(self, status: str) -> str:
        if status ==Aria2TaskStatus["ACTIVE"]:
            return DownloadStatus["DOWNLOADING"]
        if status == Aria2TaskStatus["COMPLETE"]:
            return DownloadStatus["FINISHED"]
        if status == Aria2TaskStatus["REMOVED"]:
            return DownloadStatus["ERROR"]
        return status
