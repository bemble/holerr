package api

import (
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
)

func Router(r chi.Router) {
	r.Use(middleware.SetHeader("Content-Type", "application/json"))

	r.Get(`/status`, StatusList)

	r.Get(`/downloads`, DownloadsList)
	r.Post(`/downloads`, DownloadsAdd)
	r.Delete(`/downloads/{id}`, DownloadsDelete)
	r.Post(`/downloads/clean_up`, DownloadsCleanUp)

	r.Get(`/ws`, Websocket)

	r.Get(`/presets`, PresetsList)

	r.Get(`/constants`, ConstantsList)
}
