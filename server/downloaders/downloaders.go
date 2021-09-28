package downloaders

import (
	"reflect"
	"holerr/core/log"
	"holerr/core/config"
	"holerr/downloaders/synologyDownloadStation"
	"holerr/downloaders/downloader"
)

var d downloader.Downloader = nil

func Get() downloader.Downloader {
	if d == nil {
		Config := config.Get()
		if !reflect.DeepEqual(Config.Downloaders.SynologyDownloadStation, config.SynologyDownloadStation{}) {
			log.Info("Using Synology Download Station as downloader")
			d = synologyDownloadStation.New()
		}
	}
	return d
}

