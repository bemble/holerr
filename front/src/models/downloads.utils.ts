import { DownloadStatus } from "./downloads.type";

export type DownloadStepStatus = "waiting" | "progress" | "success" | "failure";
type DownloadConfig = {
  type: "progress" | "success" | "error";
  step: number;
};

export const DEFAULT_STATUS_CONFIG: DownloadConfig = {
  type: "progress",
  step: 0,
};

export const downloadStatusConfig: Map<
  DownloadStatus,
  DownloadConfig
> = new Map([
  [
    DownloadStatus.TORRENT_FOUND,
    {
      type: "progress",
      step: 1,
    },
  ],
  [
    DownloadStatus.TORRENT_SENT_TO_DEBRIDER,
    {
      type: "progress",
      step: 2,
    },
  ],
  [
    DownloadStatus.DEBRIDER_DOWNLOADING,
    {
      type: "progress",
      step: 2,
    },
  ],
  [
    DownloadStatus.DEBRIDER_DOWNLOADED,
    {
      type: "progress",
      step: 2,
    },
  ],
  [
    DownloadStatus.SENT_TO_DOWNLOADER,
    {
      type: "progress",
      step: 3,
    },
  ],
  [
    DownloadStatus.DOWNLOADER_DOWNLOADING,
    {
      type: "progress",
      step: 3,
    },
  ],
  [
    DownloadStatus.DOWNLOADER_DOWNLOADED,
    {
      type: "success",
      step: 3,
    },
  ],
  [
    DownloadStatus.ERROR_NO_FILES_FOUND,
    {
      type: "error",
      step: 1,
    },
  ],
  [
    DownloadStatus.ERROR_DEBRIDER,
    {
      type: "error",
      step: 2,
    },
  ],
  [
    DownloadStatus.ERROR_DOWNLOADER,
    {
      type: "error",
      step: 3,
    },
  ],
  [
    DownloadStatus.STOPPED,
    {
      type: "error",
      step: 0,
    },
  ],
]);
