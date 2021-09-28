package debriders

import (
	"reflect"
	"holerr/core/config"
	"holerr/core/log"
	"holerr/debriders/debrider"
	"holerr/debriders/realdebrid"
)

var d debrider.Debrider = nil

func Get() debrider.Debrider {
	if d == nil {
		Config := config.Get()
		if !reflect.DeepEqual(Config.Debriders.RealDebrid, config.RealDebrid{}) {
			log.Info("Using real-debrid as torrent downloader/debrider")
			d = realdebrid.New()
		}
	}
	return d
}
