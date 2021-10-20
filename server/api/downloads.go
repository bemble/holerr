package api

import (
	"encoding/json"
	"fmt"
	"holerr/core/config"
	"holerr/core/db"
	"holerr/core/log"
	"holerr/debriders"
	"holerr/downloaders"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"reflect"
	"strings"

	"github.com/go-chi/chi"
)

func DownloadsList(w http.ResponseWriter, r *http.Request) {
	dbi := db.Get()
	records, err := dbi.ReadAll("downloads")
	if err != nil {
		log.Error(err)
	}

	downloads := []db.Download{}
	for _, f := range records {
		down := db.Download{}
		if err := json.Unmarshal([]byte(f), &down); err != nil {
			log.Error(err)
		}
		downloads = append(downloads, down)
	}

	body, _ := json.Marshal(downloads)
	w.Write(body)
}

func DownloadsAdd(w http.ResponseWriter, r *http.Request) {
	r.ParseMultipartForm(32 << 20)

	// Read form fields
	presetName := r.FormValue("preset")
	preset, err := config.GetPresetByName(presetName)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		body, _ := json.Marshal(map[string]string{"message": err.Error()})
		w.Write(body)
		return
	}

	// Source
	file, handler, err := r.FormFile("torrent_file")
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		body, _ := json.Marshal(map[string]string{"message": err.Error()})
		w.Write(body)
		return
	}
	defer file.Close()

	// Destination
	outputFilePath := filepath.Clean(fmt.Sprintf(`%s/%s/%s`, config.GetDataDir(), preset.WatchDir, handler.Filename))
	dst, err := os.Create(outputFilePath)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		body, _ := json.Marshal(map[string]string{"message": err.Error()})
		w.Write(body)
		return
	}
	defer dst.Close()

	// Copy
	if _, err = io.Copy(dst, file); err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		body, _ := json.Marshal(map[string]string{"message": err.Error()})
		w.Write(body)
		return
	}

	body, _ := json.Marshal(map[string]string{})
	w.Write(body)
}

func DownloadsDelete(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")
	dbi := db.Get()
	down := db.Download{}
	dbi.Read("downloads", id, &down)
	if reflect.DeepEqual(down, db.Download{}) {
		w.WriteHeader(http.StatusInternalServerError)
		body, _ := json.Marshal(map[string]string{"message": "Download not found"})
		w.Write(body)
		return
	}

	// Torrent found
	if down.Status == db.DownloadStatus["TORRENT_FOUND"] {
		// Do nothing, too early, torrent is added just after
	}

	// Debrider
	if down.Status >= db.DownloadStatus["TORRENT_SENT_TO_DEBRIDER"] && down.Status <= db.DownloadStatus["DEBRIDER_DOWNLOADED"] {
		debrider := debriders.Get()
		if debrider != nil {
			err := debrider.DeleteTorrent(down.TorrentInfo.Id)
			if err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				body, _ := json.Marshal(map[string]string{"message": "Could not delete torrent on debrider"})
				w.Write(body)
				return
			}
		} else {
			w.WriteHeader(http.StatusInternalServerError)
			body, _ := json.Marshal(map[string]string{"message": "No debrider set"})
			w.Write(body)
		}
	}

	// Downloader
	if down.Status >= db.DownloadStatus["SENT_TO_DOWNLOADER"] && down.Status <= db.DownloadStatus["DOWNLOADER_DOWNLOADED"] {
		ids := make([]string, 0, len(down.DownloadInfo.Tasks))
		for _, task := range down.DownloadInfo.Tasks {
			ids = append(ids, task.Id)
		}

		if len(ids) == 0 {
			w.WriteHeader(http.StatusInternalServerError)
			body, _ := json.Marshal(map[string]string{"message": "No download task to delete"})
			w.Write(body)
			return
		}

		downloader := downloaders.Get()
		if downloader != nil {
			err := downloader.DeleteDownload(strings.Join(ids, ","))
			if err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				body, _ := json.Marshal(map[string]string{"message": "Could not delete download task on downloader"})
				w.Write(body)
				return
			}
		} else {
			w.WriteHeader(http.StatusInternalServerError)
			body, _ := json.Marshal(map[string]string{"message": "No downloader set"})
			w.Write(body)
		}
	}

	if writeErr := dbi.Delete("downloads", id); writeErr != nil {
		w.WriteHeader(http.StatusInternalServerError)
		body, _ := json.Marshal(map[string]string{"message": "Could not delete download in database"})
		w.Write(body)
		return
	}

	WebsocketBroadcast("downloads/delete", down)

	body, _ := json.Marshal(map[string]string{})
	w.Write(body)
}

func DownloadsCleanUp(w http.ResponseWriter, r *http.Request) {
	dbi := db.Get()
	records, err := dbi.ReadAll("downloads")
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		body, _ := json.Marshal(map[string]string{"message": err.Error()})
		w.Write(body)
		return
	}

	downloads := []db.Download{}
	for _, f := range records {
		down := db.Download{}
		if err := json.Unmarshal([]byte(f), &down); err != nil {
			log.Error(err)
		}
		if down.Status >= db.DownloadStatus["DOWNLOADER_DOWNLOADED"] {
			errRemove := dbi.Delete("downloads", down.Id)
			if errRemove != nil {
				log.Error(errRemove)
			}
			downloads = append(downloads, down)

			WebsocketBroadcast("downloads/delete", down)
		}
	}

	body, _ := json.Marshal(downloads)
	w.Write(body)
}
