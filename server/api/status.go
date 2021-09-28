package api

import (
	"encoding/json"
	"net/http"
	"holerr/debriders"
	"holerr/downloaders"
)

func StatusList(w http.ResponseWriter, r *http.Request) {
	debrider := debriders.Get()
	debriderStatus := debrider.IsConnected()

	downloader := downloaders.Get()
	downloaderStatus := downloader.IsConnected()

	var list = map[string]interface{}{
		"debrider_connected": debriderStatus,
		"downloader_connected":  downloaderStatus,
	}
	body, _ := json.Marshal(list)
	w.Write(body)
}
