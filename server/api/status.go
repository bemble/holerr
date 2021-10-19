package api

import (
	"encoding/json"
	"holerr/debriders"
	"holerr/downloaders"
	"net/http"
)

func StatusList(w http.ResponseWriter, r *http.Request) {
	debriderStatus := false
	debrider := debriders.Get()
	if debrider != nil {
		debriderStatus = debrider.IsConnected()
	}

	downloaderStatus := false
	downloader := downloaders.Get()
	if downloader != nil {
		downloaderStatus = downloader.IsConnected()
	}

	var list = map[string]interface{}{
		"debrider_connected":   debriderStatus,
		"downloader_connected": downloaderStatus,
	}
	body, _ := json.Marshal(list)
	w.Write(body)
}
