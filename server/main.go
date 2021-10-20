package main

import (
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"holerr/api"
	"holerr/core/config"
	"holerr/core/log"
	"holerr/debriders"
	"holerr/downloaders"
	"holerr/scheduler"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func init() {
	log.Error("init")
	config.InitFromFile()

	log.Info("Service RUN on DEBUG mode")

	debrider := debriders.Get()
	if debrider != nil {
		log.Info("Using debrider " + debrider.GetName() + "")
	}

	downloader := downloaders.Get()
	if downloader != nil {
		log.Info("Using downloader " + downloader.GetName())
	}
}

func main() {
	log.Error("main")

	// Scheduler
	go func() {
		scheduler.Downloads()
	}()

	r := chi.NewRouter()

	// A good base middleware stack
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	if config.IsDebug() {
		r.Use(middleware.Logger)
	}
	r.Use(middleware.Recoverer)

	basePath := config.GetBasePath()
	if basePath == "" {
		config.SetBasePath("/")
		basePath = "/"
	}
	if basePath != "/" && basePath[len(basePath)-1] != '/' {
		r.Get(basePath, http.RedirectHandler(basePath+"/", 301).ServeHTTP)
		basePath += "/"
	}

	r.Get(basePath+"*", func(w http.ResponseWriter, r *http.Request) {
		requestUri := "/" + strings.TrimPrefix(r.RequestURI, basePath)
		staticHandler := http.FileServer(http.Dir(config.GetPublicDir()))
		fs := http.StripPrefix(basePath, staticHandler)
		if _, err := os.Stat(filepath.Join(config.GetPublicDir(), requestUri)); os.IsNotExist(err) {
			// If not exists, fallback on index.html
			http.ServeFile(w, r, filepath.Join(config.GetPublicDir(), "index.html"))
		} else {
			// If file exists in public dir, serve it
			fs.ServeHTTP(w, r)
		}
	})

	r.Route(basePath+"api", api.Router)

	log.Fatal(http.ListenAndServe(":8781", r))
	log.Info("Server started: http://0.0.0.0:8781")
}
