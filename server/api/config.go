package api

import (
	"encoding/json"
	"github.com/spf13/viper"
	"holerr/core/config"
	"log"
	"net/http"
	"strings"
)

func hideSecret(s string) string {
	return s[0:1] + strings.Repeat("*", len(s)-2) + s[len(s)-1:]
}

func ConfigList(w http.ResponseWriter, r *http.Request) {
	list := map[string]interface{}{
		config.ConfKeyDebug:    config.IsDebug(),
		config.ConfKeyApiKey:   config.GetApiKey(),
		config.ConfKeyBasePath: config.GetBasePath(),
	}

	debriders, debridersErr := config.GetDebriders()
	if debridersErr == nil {
		if debriders.RealDebrid.ApiKey != "" {
			debriders.RealDebrid.ApiKey = hideSecret(debriders.RealDebrid.ApiKey)
		}
		list[config.ConfKeyDebriders] = debriders
	}

	downloaders, downloadersErr := config.GetDownloaders()
	if downloadersErr == nil {
		if downloaders.SynologyDownloadStation.Password != "" {
			downloaders.SynologyDownloadStation.Password = hideSecret(downloaders.SynologyDownloadStation.Password)
		}
		list[config.ConfKeyDownloaders] = downloaders
	}

	body, _ := json.Marshal(list)
	w.Write(body)
}

func ConfigUpdate(w http.ResponseWriter, r *http.Request) {
	decodeError := viper.MergeConfig(r.Body)
	if decodeError != nil {
		log.Println(decodeError)
		w.WriteHeader(http.StatusInternalServerError)
		content := map[string]error{
			"message": decodeError,
		}
		body, _ := json.Marshal(content)
		w.Write(body)
	} else {
		viper.WriteConfig()
		config.SetBasePath(config.GetBasePath())
		config.SetApiKey(config.GetApiKey())
		ConfigList(w, r)
	}
}
