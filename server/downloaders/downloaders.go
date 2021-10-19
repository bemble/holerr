package downloaders

import (
	"holerr/core/config"
	"holerr/core/log"
	"holerr/downloaders/downloader"
	"holerr/downloaders/synologyDownloadStation"
	"reflect"
)

var d downloader.Downloader = nil

func Get() downloader.Downloader {
	if d == nil {
		downloaders, err := config.GetDownloaders()
		if !(err || reflect.DeepEqual(downloaders.SynologyDownloadStation, config.SynologyDownloadStation{})) {
			log.Info("Using Synology Download Station as downloader")
			d = synologyDownloadStation.New()
		}
	}
	return d
}
