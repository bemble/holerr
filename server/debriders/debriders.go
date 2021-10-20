package debriders

import (
	"holerr/core/config"
	"holerr/debriders/debrider"
	"holerr/debriders/realdebrid"
)

var d debrider.Debrider = nil

func Get() debrider.Debrider {
	if d == nil {
		_, err := config.GetRealDebrid()
		if err == nil {
			d = realdebrid.New()
		}
	}
	return d
}
