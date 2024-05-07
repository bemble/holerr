export enum DownloadStatus {
  TORRENT_FOUND = 0,
  TORRENT_SENT_TO_DEBRIDER = 10,
  DEBRIDER_DOWNLOADING = 11,
  DEBRIDER_POST_DOWNLOAD = 12,
  DEBRIDER_DOWNLOADED = 13,
  SENT_TO_DOWNLOADER = 20,
  DOWNLOADER_DOWNLOADING = 21,
  DOWNLOADER_DOWNLOADED = 22,
  DOWNLOADED = 30,
  ERROR_NO_FILES_FOUND = 100,
  ERROR_DEBRIDER = 101,
  ERROR_DOWNLOADER = 102,
  ERROR_DELETED_ON_DEBRIDER = 103,
}

export type Download = {
  id: string;
  title: string;
  preset: string;
  status: DownloadStatus;
  total_bytes: number;
  total_progress: number;
  to_delete: boolean;
  created_at: string;
  updated_at: string;
};
