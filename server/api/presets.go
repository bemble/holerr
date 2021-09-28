package api

import (
	"encoding/json"
	"net/http"
	"holerr/core/config"
)

func PresetsList(w http.ResponseWriter, r *http.Request) {
	cfg := config.Get()

	body, _ := json.Marshal(cfg.Presets)
	w.Write(body)
}
