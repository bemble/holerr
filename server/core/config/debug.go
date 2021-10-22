package config

import (
	"github.com/spf13/viper"
)

func IsDebug() bool {
	return viper.GetBool(ConfKeyDebug)
}
