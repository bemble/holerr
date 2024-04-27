from .download_state_transitions import TaskDownloadStateTransition
from .torrent_files import TaskTorrentFiles
from .debrider import TaskDebrider
from .downloader import TaskDownloader

download_state_transitions = TaskDownloadStateTransition()
torrent_files = TaskTorrentFiles()
debrider = TaskDebrider()
downloader = TaskDownloader()
