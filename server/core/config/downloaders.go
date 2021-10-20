package config

import (
	"errors"
	"github.com/spf13/viper"
	"reflect"
)

func GetDownloaders() (Downloaders, error) {
	if viper.IsSet(ConfKeyDownloaders) {
		downloaders := Downloaders{}
		err := viper.UnmarshalKey(ConfKeyDownloaders, &downloaders)
		if err == nil {
			return downloaders, nil
		}
	}
	return Downloaders{}, errors.New("No downloader set")
}

func GetSynologyDownloadStation() (SynologyDownloadStation, error) {
	downloaders, err := GetDownloaders()
	if err == nil && !(reflect.DeepEqual(downloaders.SynologyDownloadStation, SynologyDownloadStation{})) {
		return downloaders.SynologyDownloadStation, nil
	}
	return SynologyDownloadStation{}, errors.New("Synology downloader not set")
}
