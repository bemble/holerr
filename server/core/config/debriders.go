package config

import (
	"github.com/spf13/viper"
	"reflect"
)

func GetDebriders() (Debriders, bool) {
	if viper.IsSet(ConfKeyDebriders) {
		debriders := Debriders{}
		err := viper.UnmarshalKey(ConfKeyDebriders, &debriders)
		if err == nil {
			return debriders, false
		}
	}
	return Debriders{}, true
}

func GetRealDebrid() (RealDebrid, bool) {
	debriders, err := GetDebriders()
	if !(err || reflect.DeepEqual(debriders.RealDebrid, RealDebrid{})) {
		return debriders.RealDebrid, false
	}
	return RealDebrid{}, true
}

func SetRealDebrid(debrid RealDebrid) {
	debriders, _ := GetDebriders()
	debriders.RealDebrid = debrid
	viper.Set(ConfKeyDebriders, debriders)
	viper.WriteConfig()
}
