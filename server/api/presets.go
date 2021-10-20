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
	preset := config.Preset{}
	decodeErr := json.NewDecoder(r.Body).Decode(&preset)

	if decodeErr != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Decode error: " + decodeErr.Error()))
		return
	}

	addErr := config.AddPreset(preset)
	if addErr != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(addErr.Error()))
		return
	}

	preset, _ = config.GetPresetByName(preset.Name)
	body, _ := json.Marshal(preset)
	w.Write(body)
}

func PresetsUpdate(w http.ResponseWriter, r *http.Request) {
	name := chi.URLParam(r, "name")

	preset := config.Preset{}
	decodeErr := json.NewDecoder(r.Body).Decode(&preset)

	if decodeErr != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Decode error: " + decodeErr.Error()))
		return
	}

	updateErr := config.UpdatePreset(name, preset)
	if updateErr != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(updateErr.Error()))
		return
	}

	newName := name
	if preset.Name != "" {
		newName = preset.Name
	}
	preset, _ = config.GetPresetByName(newName)
	body, _ := json.Marshal(preset)
	w.Write(body)
}

func PresetsDelete(w http.ResponseWriter, r *http.Request) {
	name := chi.URLParam(r, "name")
	config.RemovePreset(name)
	w.WriteHeader(http.StatusNoContent)
}
