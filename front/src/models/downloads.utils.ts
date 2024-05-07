import { DownloadStatus } from "./downloads.type";

export enum DownloadStepStatus {
  WAITING = "waiting",
  PROGRESS = "progress",
  SUCCESS = "success",
  FAILURE = "failure",
}

export enum DownloadStep {
  UNKNOWN,
  DEBRIDER,
  DOWNLOADER,
  GENERAL,
}
type DownloadConfig = {
  status: DownloadStepStatus;
  step: DownloadStep;
};

export const DEFAULT_STATUS_CONFIG: DownloadConfig = {
  status: DownloadStepStatus.WAITING,
  step: DownloadStep.UNKNOWN,
};

export const downloadStatusConfig: Map<DownloadStatus, DownloadConfig> =
  new Map([
    [
      DownloadStatus.TORRENT_FOUND,
      {
        status: DownloadStepStatus.PROGRESS,
        step: DownloadStep.GENERAL,
      },
    ],
    [
      DownloadStatus.TORRENT_SENT_TO_DEBRIDER,
      {
        status: DownloadStepStatus.PROGRESS,
        step: DownloadStep.DEBRIDER,
      },
    ],
    [
      DownloadStatus.DEBRIDER_DOWNLOADING,
      {
        status: DownloadStepStatus.PROGRESS,
        step: DownloadStep.DEBRIDER,
      },
    ],
    [
      DownloadStatus.DEBRIDER_POST_DOWNLOAD,
      {
        status: DownloadStepStatus.PROGRESS,
        step: DownloadStep.DEBRIDER,
      },
    ],
    [
      DownloadStatus.DEBRIDER_DOWNLOADED,
      {
        status: DownloadStepStatus.PROGRESS,
        step: DownloadStep.DEBRIDER,
      },
    ],
    [
      DownloadStatus.SENT_TO_DOWNLOADER,
      {
        status: DownloadStepStatus.PROGRESS,
        step: DownloadStep.DOWNLOADER,
      },
    ],
    [
      DownloadStatus.DOWNLOADER_DOWNLOADING,
      {
        status: DownloadStepStatus.PROGRESS,
        step: DownloadStep.DOWNLOADER,
      },
    ],
    [
      DownloadStatus.DOWNLOADER_DOWNLOADED,
      {
        status: DownloadStepStatus.SUCCESS,
        step: DownloadStep.DOWNLOADER,
      },
    ],
    [
      DownloadStatus.DOWNLOADED,
      {
        status: DownloadStepStatus.SUCCESS,
        step: DownloadStep.GENERAL,
      },
    ],
    [
      DownloadStatus.ERROR_NO_FILES_FOUND,
      {
        status: DownloadStepStatus.FAILURE,
        step: DownloadStep.DEBRIDER,
      },
    ],
    [
      DownloadStatus.ERROR_DEBRIDER,
      {
        status: DownloadStepStatus.FAILURE,
        step: DownloadStep.DEBRIDER,
      },
    ],
    [
      DownloadStatus.ERROR_DOWNLOADER,
      {
        status: DownloadStepStatus.FAILURE,
        step: DownloadStep.DOWNLOADER,
      },
    ],
    [
      DownloadStatus.ERROR_DELETED_ON_DEBRIDER,
      {
        status: DownloadStepStatus.FAILURE,
        step: DownloadStep.DEBRIDER,
      },
    ],
  ]);
