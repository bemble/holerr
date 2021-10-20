package config

import (
	"errors"
	"github.com/spf13/viper"
	"reflect"
)

func GetDebriders() (Debriders, error) {
	if viper.IsSet(ConfKeyDebriders) {
		debriders := Debriders{}
		err := viper.UnmarshalKey(ConfKeyDebriders, &debriders)
		if err == nil {
			return debriders, nil
		}
	}
	return Debriders{}, errors.New("No debrider set")
}

func GetRealDebrid() (RealDebrid, error) {
	debriders, err := GetDebriders()
	if err == nil && !(reflect.DeepEqual(debriders.RealDebrid, RealDebrid{})) {
		return debriders.RealDebrid, nil
	}
	return RealDebrid{}, errors.New("Real-Debrid not set")
}
