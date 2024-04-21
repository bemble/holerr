from server.core import config

config.load()

from server.core.config_repositories import PresetRepository

PresetRepository.create_directories()

from server.debriders import debrider

if not debrider.is_connected():
    raise Exception("Debrider not connected")
