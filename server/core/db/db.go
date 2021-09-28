package db

import (
	"fmt"
	scribble "github.com/nanobox-io/golang-scribble"
	"os"
	"path/filepath"
	"holerr/core/config"
	"holerr/core/log"
)

var db *scribble.Driver
var inited bool = false

func Get() *scribble.Driver {
	if !isInited() {
		log.Info("Initing database...")
		createDbDirs()

		dbDir := fmt.Sprintf(`%s/db`, config.GetDataDir())
		ndb, err := scribble.New(dbDir, nil)
		if err != nil {
			log.Fatal(err)
		}
		db = ndb
		inited = true
	}
	return db
}

func isInited() bool {
	return inited
}

func createDbDirs() {
	dbDir := fmt.Sprintf(`%s/db`, config.GetDataDir())
	newpath := filepath.Join(dbDir, "downloads")
	os.MkdirAll(newpath, os.ModePerm)
}
