package api

import (
	"encoding/json"
	"github.com/go-chi/chi"
	"holerr/core/config"
	"net/http"
)

func PresetsList(w http.ResponseWriter, r *http.Request) {
	presets, _ := config.GetPresets()

	body, _ := json.Marshal(presets)
	w.Write(body)
}

func PresetsAdd(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusInternalServerError)
	w.Write([]byte("Not implemented yet"))
}

func PresetsUpdate(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusInternalServerError)
	w.Write([]byte("Not implemented yet"))
}

func PresetsDelete(w http.ResponseWriter, r *http.Request) {
	name := chi.URLParam(r, "name")
	config.RemovePreset(name)
	w.WriteHeader(http.StatusNoContent)
}
