package scheduler

import (
	"time"
	"holerr/core/db"
	"holerr/core/log"
	"holerr/debriders"
	debriderInterface "holerr/debriders/debrider"
)

func UpdateDebriderInfos(download *db.Download) {
	dbi := db.Get()
	debrider := debriders.Get()

	previousStatus := download.Status

	var err error
	download.TorrentInfo, err = debrider.GetTorrentInfos(download.TorrentInfo.Id)
	if err != nil {
		log.Error(err)
	}
	if download.TorrentInfo.Status == debriderInterface.TorrentStatus["DOWNLOADED"] {
		download.Status = db.DownloadStatus["DEBRIDER_DOWNLOADED"]
	} else if download.TorrentInfo.Status == debriderInterface.TorrentStatus["ERROR"] || download.TorrentInfo.Status == debriderInterface.TorrentStatus["VIRUS"] || download.TorrentInfo.Status == debriderInterface.TorrentStatus["DEAD"] {
		download.Status = db.DownloadStatus["ERROR_DEBRIDER"]
	} else {
		download.Status = db.DownloadStatus["DEBRIDER_DOWNLOADING"]
	}

	if previousStatus != download.Status {
		download.StatusDetails = db.DownloadStatusDetail[download.Status]
		download.UpdatedAt = time.Now()
	}

	if writeErr := dbi.Write("downloads", download.Id, download); writeErr != nil {
		log.Error(writeErr)
	}
}
