from server.core import config

config.load()

from server.core.log import Log

log = Log.get_logger(__name__)

from server.core.config_repositories import PresetRepository

PresetRepository.create_watch_directories()

from server.debriders import debrider

if not debrider.is_connected():
    log.info("Debrider not connected")

from server.downloaders import downloader

if not downloader.is_connected():
    log.info("Downloader not connected")
