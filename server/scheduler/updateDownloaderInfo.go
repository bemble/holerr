package scheduler

import (
	"time"
	"holerr/core/db"
	"holerr/core/log"
	"holerr/downloaders"
)

func UpdateDownloaderInfo(download *db.Download) {
	previousUpdatedAt := download.UpdatedAt

	downloader := downloaders.Get()
	dbi := db.Get()

	// Do not ask all at once, status is messy (first is a valid status, others are int)
	downloadStatus := db.DownloadStatus["DOWNLOADER_DOWNLOADED"]
	totalBytesDownloaded := 0
	for uri, task := range download.DownloadInfo.Tasks {
		if task.Status != db.DownloadStatus["DOWNLOADER_DOWNLOADED"] && task.Status != db.DownloadStatus["ERROR_DOWNLOADER"] {
			taskStatus, sizeDownloaded, err := downloader.GetTaskStatus(task.Id)
			task.Status = taskStatus
			task.BytesDownloaded = sizeDownloaded
			if downloadStatus != db.DownloadStatus["ERROR_DOWNLOADER"] {
				if err != nil {
					log.Error(err)
					downloadStatus = db.DownloadStatus["ERROR_DOWNLOADER"]
				}

				if taskStatus < downloadStatus || taskStatus == db.DownloadStatus["ERROR_DOWNLOADER"] {
					downloadStatus = taskStatus
				}
			}
			download.DownloadInfo.Tasks[uri] = task
			download.UpdatedAt = time.Now()
		}
		totalBytesDownloaded += task.BytesDownloaded
	}

	if download.UpdatedAt != previousUpdatedAt {
		download.DownloadInfo.Progress = int((totalBytesDownloaded * 100 / download.DownloadInfo.Bytes))
		download.Status = downloadStatus
		download.StatusDetails = db.DownloadStatusDetail[download.Status]
		if writeErr := dbi.Write("downloads", download.Id, download); writeErr != nil {
			log.Error(writeErr)
		}
	}
}
