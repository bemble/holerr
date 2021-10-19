package main

import (
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"holerr/api"
	"holerr/core/config"
	"holerr/core/log"
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

/*	if reflect.DeepEqual(Config.Presets, []int{}) || Config.Presets == nil {
		log.Fatal("No preset configured")
	}

	db.Get()

	debrider := debriders.Get()
	if reflect.DeepEqual(Config.Debriders, config.Debriders{}) || debrider == nil {
		log.Fatal("No debrider configured")
	}
	myProfile, err := debrider.Me()
	if err != nil {
		panic(err)
	}
	log.Info("Debrider user: " + myProfile)

	downloader := downloaders.Get()
	if reflect.DeepEqual(Config.Downloaders, config.Downloaders{}) || downloader == nil {
		log.Fatal("No downloader configured")
	}
 */
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
