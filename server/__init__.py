from server.core.config import config
from server.core.config_repositories import PresetRepository

config.load()
PresetRepository.create_directories()
