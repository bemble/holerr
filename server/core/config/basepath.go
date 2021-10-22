package config

import (
	"github.com/spf13/viper"
	"holerr/core/tools/placeholder"
)

const BasePathPlaceholder = "%holerr-base-path-placeholder%"

func GetBasePath() string {
	return viper.GetString(ConfKeyBasePath)
}

func SetBasePath(base_path string) {
	viper.Set(ConfKeyBasePath, base_path)
	viper.WriteConfig()

	replacer := placeholder.Replacer{
		Placeholder: BasePathPlaceholder,
		Replacement: base_path,
		IsURLPath: true,
	}
	placeholder.SetReplacer(replacer)

	placeholder.ReplaceInFiles(GetPublicDir())
}
