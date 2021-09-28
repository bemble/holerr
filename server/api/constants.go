package api

import (
	"encoding/json"
	"net/http"
	"holerr/core/db"
	"holerr/debriders/debrider"
)

func ConstantsList(w http.ResponseWriter, r *http.Request) {
	var list = map[string]interface{}{
		"download_status": db.DownloadStatus,
		"torrent_status":  debrider.TorrentStatus,
	}
	body, _ := json.Marshal(list)
	w.Write(body)
}
