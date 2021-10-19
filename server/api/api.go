package api

import (
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
)

func Router(r chi.Router) {
	r.Use(middleware.SetHeader("Content-Type", "application/json"))

	r.Get(`/status`, StatusList)
	r.Post(`/server/restart`, ServerRestart)

	r.Get(`/configuration`, ConfigList)
	r.Patch(`/configuration`, ConfigUpdate)

	r.Get(`/downloads`, DownloadsList)
	r.Post(`/downloads`, DownloadsAdd)
	r.Delete(`/downloads/{id}`, DownloadsDelete)
	r.Post(`/downloads/clean_up`, DownloadsCleanUp)

	r.Get(`/ws`, Websocket)

	r.Get(`/presets`, PresetsList)
	r.Post(`/presets`, PresetsAdd)
	r.Patch(`/presets/{name}`, PresetsUpdate)
	r.Delete(`/presets/{name}`, PresetsDelete)

	r.Get(`/constants`, ConstantsList)
}
