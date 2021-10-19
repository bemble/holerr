package config

import (
	"github.com/spf13/viper"
	"reflect"
)

func GetDownloaders() (Downloaders, bool) {
	if viper.IsSet(ConfKeyDownloaders) {
		downloaders := Downloaders{}
		err := viper.UnmarshalKey(ConfKeyDownloaders, &downloaders)
		if err == nil {
			return downloaders, false
		}
	}
	return Downloaders{}, true
}

func GetSynologyDownloadStation() (SynologyDownloadStation, bool) {
	downloaders, err := GetDownloaders()
	if !(err || reflect.DeepEqual(downloaders.SynologyDownloadStation, SynologyDownloadStation{})) {
		return downloaders.SynologyDownloadStation, false
	}
	return SynologyDownloadStation{}, true
}

func SetSynologyDownloadStation(downloader SynologyDownloadStation) {
	downloaders, _ := GetDownloaders()
	downloaders.SynologyDownloadStation = downloader
	viper.Set(ConfKeyDownloaders, downloaders)
	viper.WriteConfig()
}
