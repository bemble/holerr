package debriders

import (
	"holerr/core/config"
	"holerr/core/log"
	"holerr/debriders/debrider"
	"holerr/debriders/realdebrid"
)

var d debrider.Debrider = nil

func Get() debrider.Debrider {
	if d == nil {
		_, confError := config.GetRealDebrid()
		if !confError {
			log.Info("Using real-debrid as torrent downloader/debrider")
			d = realdebrid.New()
		}
	}
	return d
}
