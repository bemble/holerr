package scheduler

import (
	"encoding/json"
	"reflect"
	"time"
	"holerr/api"
	"holerr/core/db"
	"holerr/core/log"
	"holerr/debriders/debrider"
)

func Downloads() {
	dbi := db.Get()

	for {
		AddTorrents()

		records, err := dbi.ReadAll("downloads")
		if err != nil {
			log.Error(err)
		}

		for _, f := range records {
			downloadBeforeOperation := db.Download{}
			if err := json.Unmarshal([]byte(f), &downloadBeforeOperation); err != nil {
				log.Error(err)
			}

			download := db.Download{}
			if err := json.Unmarshal([]byte(f), &download); err != nil {
				log.Error(err)
			}

			if download.Status == db.DownloadStatus["TORRENT_SENT_TO_DEBRIDER"] && download.TorrentInfo.Status == debrider.TorrentStatus["WAITING_FILES_SELECTION"] {
				SelectFiles(&download)
			}

			if download.Status == db.DownloadStatus["DEBRIDER_DOWNLOADING"] {
				UpdateDebriderInfos(&download)
			}

			if download.Status == db.DownloadStatus["DEBRIDER_DOWNLOADED"] {
				DownloadFiles(&download)
			}

			if download.Status == db.DownloadStatus["SENT_TO_DOWNLOADER"] || download.Status == db.DownloadStatus["DOWNLOADER_DOWNLOADING"] {
				UpdateDownloaderInfo(&download)
			}

			// Send change notification if change detected
			if !reflect.DeepEqual(downloadBeforeOperation, download) {
				api.WebsocketBroadcast("downloads/update", download)
			}
		}
		time.Sleep(5 * time.Second)
	}
}
