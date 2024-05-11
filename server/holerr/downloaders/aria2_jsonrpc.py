from .downloader import Downloader
from holerr.core import config
from holerr.core.log import Log
from .aria2_jsonrpc_models import Status, StatusResult
from holerr.core.config_models import Preset
from holerr.core.exceptions import HttpRequestException

from typing import Any
import requests
from pathlib import Path
import urllib
import json
import uuid

log = Log.get_logger(__name__)


class Aria2JsonRpc(Downloader):
    def __init__(self):
        # TODO: handle websocket when endpoints starts with ws:// or wss://
        pass

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
        pass

    def get_task_status(self, id: str) -> tuple[str, int]:
        pass

    def delete_download(self, id: str):
        pass

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

    def _get_global_status(self) -> StatusResult:
        payload = {
            "method": "aria2.getGlobalStat",
        }
        res = self._call(payload)
        if res.status_code != 200:
            raise HttpRequestException("Error while getting global status", res.status_code)
        return Status(**res.json()).result

    @staticmethod
    def compute_call_id() -> str:
        return f"holerr.{str(uuid.uuid4())}"
