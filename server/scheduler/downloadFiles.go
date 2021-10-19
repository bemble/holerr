package scheduler

import (
	"holerr/core/config"
	"holerr/core/db"
	"holerr/core/log"
	"holerr/debriders"
	"holerr/downloaders"
)

func DownloadFiles(download *db.Download) {
	downloader := downloaders.Get()
	if downloader == nil {
		log.Error("No downloader configured")
		return
	}

	preset, err := config.GetPresetByName(download.Preset)
	if err != nil {
		log.Error(err)
		return
	}
	downloadInfo := db.DownloadInfo{Progress: 0, Bytes: 0, Tasks: map[string]db.DownloadInfoTask{}}
	for _, file := range download.TorrentInfo.Files {
		if file.Selected == 1 {
			downloadInfo.Bytes += file.Bytes
		}
	}

	for _, link := range download.TorrentInfo.Links {
		id, err := downloader.AddDownload(link, download.Title, preset)
		if err != nil {
			log.Error(err)
		}
		downloadInfo.Tasks[link] = db.DownloadInfoTask{Id: id}
	}

	debrider := debriders.Get()
	err = debrider.DeleteTorrent(download.TorrentInfo.Id)
	if err != nil {
		log.Error(err)
	}

	dbi := db.Get()
	download.Status = db.DownloadStatus["SENT_TO_DOWNLOADER"]
	download.StatusDetails = db.DownloadStatusDetail[download.Status]
	download.DownloadInfo = downloadInfo
	if writeErr := dbi.Write("downloads", download.Id, download); writeErr != nil {
		log.Error(writeErr)
	}
}
