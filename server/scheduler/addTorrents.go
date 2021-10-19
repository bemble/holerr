package scheduler

import (
	"crypto/sha1"
	"fmt"
	"holerr/api"
	"holerr/core/config"
	"holerr/core/db"
	"holerr/core/log"
	"holerr/debriders"
	debriderInterface "holerr/debriders/debrider"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"time"
)

func AddTorrents() {
	publicDir := config.GetDataDir()
	err := filepath.Walk(publicDir,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if !info.IsDir() && strings.HasSuffix(path, ".torrent") {
				log.Info("New torrent found: " + path)
				handleTorrent(path)
			}
			return nil
		})
	if err != nil {
		log.Fatal(err)
	}
}

func handleTorrent(path string) {
	dbi := db.Get()

	name, id := computeTorrentInfo(path)

	downCheck := db.Download{}
	dbi.Read("downloads", id, &downCheck)
	if !reflect.DeepEqual(downCheck, db.Download{}) {
		log.Error("Torrent already in database!")
	} else {
		preset, err := config.GetPresetByPath(path)
		if err != nil {
			log.Error(err)
		} else {
			down := handleNewTorrentFound(id, name, preset)
			sendToDebrider(path, &down)

			api.WebsocketBroadcast("downloads/new", down)
		}
	}
	err := os.Remove(path)
	if err != nil {
		log.Error(err)
	}
}

func computeTorrentInfo(path string) (string, string) {
	basename := filepath.Base(path)
	// Remove .torrent in file name
	name := basename[0 : len(basename)-8]
	h := sha1.New()
	h.Write([]byte(name))
	id := fmt.Sprintf("%x", h.Sum(nil))[1:8]

	return name, id
}

func handleNewTorrentFound(id string, name string, preset config.Preset) db.Download {
	dbi := db.Get()
	now := time.Now()
	down := db.Download{
		Id:          id,
		Title:       name,
		Preset:      preset.Name,
		Status:      db.DownloadStatus["TORRENT_FOUND"],
		TorrentInfo: debriderInterface.TorrentInfo{},
		CreatedAt:   now,
		UpdatedAt:   now,
	}
	down.StatusDetails = db.DownloadStatusDetail[down.Status]
	if writeErr := dbi.Write("downloads", id, down); writeErr != nil {
		log.Error(writeErr)
	}

	return down
}

func sendToDebrider(path string, down *db.Download) {
	dbi := db.Get()
	debrider := debriders.Get()

	if debrider == nil {
		log.Error("No debrider configured")
		return
	}

	torrentId, err := debrider.AddTorrent(path)
	if err != nil {
		log.Error(err)
	}
	down.Status = db.DownloadStatus["TORRENT_SENT_TO_DEBRIDER"]
	down.StatusDetails = db.DownloadStatusDetail[down.Status]
	down.TorrentInfo, err = debrider.GetTorrentInfos(torrentId)
	if err != nil {
		log.Error(err)
	}
	down.UpdatedAt = time.Now()
	if writeErr := dbi.Write("downloads", down.Id, down); writeErr != nil {
		log.Error(writeErr)
	}
}
