package api

import (
	"net/http"
	"os"
	"time"
)

func ServerRestart(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNoContent)
	time.Sleep(time.Millisecond * 200)
	os.Exit(0)
}
