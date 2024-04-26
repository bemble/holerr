from .downloader import Downloader
from server.core import config
from server.core.log import Log
from .synology_download_station_models import Auth, Tasks, Status
from server.core.config_models import Preset


import requests
from pathlib import Path
import urllib

log = Log.get_logger(__name__)


class SynologyDownloadStation(Downloader):
    def __init__(self, config):
        pass

    def get_name(self) -> str:
        return "Synology Download Station"

    def is_connected(self) -> bool:
        sid = self._connect("DownloadStation")
        return sid is not None

    def add_download(self, uri: str, title: str, preset: Preset) -> str:
        sid = self._connect("DownloadStation")
        if sid is None:
            raise Exception("Could not connect to Synology Download Station")

        params = {
            "api": "SYNO.DownloadStation.Task",
            "version": "1",
            "method": "create",
            "uri": uri,
            "_sid": sid,
        }
        if preset.output_dir is not None:
            destination = preset.output_dir
            if preset.create_sub_dir:
                sub_folder = self.get_sub_folder_name(title)
                self._create_output_dir(destination, sub_folder)
                destination += "/" + sub_folder
            params["destination"] = destination

        # known bug in Synology Download Station API fails with "+" destination
        params = urllib.parse.urlencode(params).replace("+", "%20")
        res = self._call("/DownloadStation/task.cgi", params=params)
        if res.status_code != 200:
            raise Exception("Could not add download " + res)
        obj = Status(**res.json())
        if not obj.success:
            log.debug(res.request.url)
            raise Exception("Error while adding download, code: " + str(obj.error.code))
        return self._get_download_id(uri)

    def get_task_status(self, id: str) -> tuple[str, int]:
        sid = self._connect("DownloadStation")
        if sid is None:
            raise Exception("Could not connect to Synology Download Station")

        params = {
            "api": "SYNO.DownloadStation.Task",
            "version": "1",
            "method": "getinfo",
            "additional": "transfer",
            "id": id,
            "_sid": sid,
        }
        res = self._call("/DownloadStation/task.cgi", params=params)
        if res.status_code != 200:
            raise Exception("Could not get task status " + str(res.status_code))

        obj = Tasks(**res.json())
        if not obj.success:
            raise Exception(
                "Error while getting task status, code: " + str(obj.error.code)
            )

        task = obj.data.tasks[0]

        return task.status, task.additional.transfer.size_downloaded

    def delete_download(self, id: str):
        sid = self._connect("DownloadStation")
        if sid is None:
            raise Exception("Could not connect to Synology Download Station")

        params = {
            "api": "SYNO.DownloadStation.Task",
            "version": "1",
            "method": "delete",
            "id": id,
            "_sid": sid,
        }
        res = self._call("/DownloadStation/task.cgi", params=params)
        if res.status_code != 200:
            raise Exception(
                "Could not delete download " + id + " " + str(res.status_code)
            )

    def _call(self, path, **kwargs):
        return requests.request("GET", self._get_api_url(path), **kwargs)

    def _get_api_url(self, path: str) -> str:
        return config.downloader.synology_download_station.endpoint + "/webapi" + path

    def _connect(self, session: str) -> str | None:
        syno_cfg = config.downloader.synology_download_station
        params = {
            "api": "SYNO.API.Auth",
            "version": "3",
            "session": session,
            "account": syno_cfg.username,
            "passwd": syno_cfg.password,
            "format": "sid",
            "method": "login",
        }
        res = self._call("/auth.cgi", params=params)
        if res.status_code != 200:
            raise Exception(
                "Could not login to " + session + " " + str(res.status_code)
            )

        auth = Auth(**res.json())
        return auth.data.sid or None

    def _get_download_id(self, uri: str) -> str:
        sid = self._connect("DownloadStation")
        if sid is None:
            raise Exception("Could not connect to Synology Download Station")

        params = {
            "api": "SYNO.DownloadStation.Task",
            "version": "1",
            "format": "sid",
            "method": "list",
            "additional": "detail",
            "_sid": sid,
        }

        res = self._call("/DownloadStation/task.cgi", params=params)
        if res.status_code != 200:
            raise Exception("Could not list downloads, " + str(res.status_code))
        obj = Tasks(**res.json())
        if not obj.success:
            raise Exception(
                "Error while searching download id, code: " + str(obj.error.code)
            )

        for task in obj.data.tasks:
            if task.additional.detail.uri == uri:
                return task.id
        log.debug(f"Download {uri} not found")
        return None

    def _create_output_dir(self, parent: str, name: str):
        sid = self._connect("FileStation")
        if sid is None:
            raise Exception("Could not connect to Synology File Station")

        folder_path = parent
        if folder_path[0] != "/":
            folder_path = "/" + folder_path

        params = {
            "api": "SYNO.FileStation.CreateFolder",
            "version": "2",
            "method": "create",
            "folder_path": folder_path,
            "name": name,
            "_sid": sid,
        }
        res = self._call("/entry.cgi", params=params)
        if res.status_code != 200:
            raise Exception("Could not create folder " + str(res.status_code))
        obj = Status(**res.json())
        if not obj.success and obj.error.code != 109:  # 109 = folder already exists
            log.debug(res.request.url)
            raise Exception("Error while creating folder, code: " + str(obj.error.code))

    @staticmethod
    def get_sub_folder_name(name: str) -> str:
        return Path(name).stem
