package downloaders

import (
	"holerr/core/config"
	"holerr/downloaders/downloader"
	"holerr/downloaders/synologyDownloadStation"
)

var d downloader.Downloader = nil

func Get() downloader.Downloader {
	if d == nil {
		_, err := config.GetSynologyDownloadStation()
		if err == nil {
			d = synologyDownloadStation.New()
		}
	}
	return d
}
