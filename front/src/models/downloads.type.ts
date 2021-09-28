export enum DownloadStatus {
  TORRENT_FOUND = 0,
  TORRENT_SENT_TO_DEBRIDER = 1,
  DEBRIDER_DOWNLOADING = 2,
  DEBRIDER_DOWNLOADED = 3,
  SENT_TO_DOWNLOADER = 4,
  DOWNLOADER_DOWNLOADING = 5,
  DOWNLOADER_DOWNLOADED = 6,
  ERROR_NO_FILES_FOUND = 100,
  ERROR_DEBRIDER = 101,
  ERROR_DOWNLOADER= 102,
  STOPPED = 200,
}

export type Download = {
  // Internal download id
  id: string;
  // Download title (computed from torrent file name)
  title: string;
  // Name of the preset used
  preset: string;
  // Global downlaod task status
  status: DownloadStatus;
  // Human readable status
  status_details: string;
  // Debrider torrent info (might have more data, according to the debrider used)
  torrent_info: TorrentInfo | null;
  // Downloader downloads info
  download_info: DownloadInfo | null;
  // Download task creation date
  created_at: string;
  // Download task last update date
  updated_at: string;
};

export type TorrentInfo = {
  id: string;
  filename: string;
  bytes: number;
  progress: number;
  status: string;
  files: DownloadFile[] | null;
  links: string[] | null;
};

export type DownloadFile = {
  id: number;
  path: string;
  bytes: number;
  selected: number;
};

export type DownloadInfo = {
  progress: number;
  // Key are links, values are downloader id
  tasks: Record<string, DownloadInfoTask>
};

export type DownloadInfoTask = {
  id: string;
  status: number;
  bytes: number;
  bytes_downloaded: number;
};