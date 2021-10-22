package config

import (
	"github.com/spf13/viper"
	"holerr/core/tools/placeholder"
)

const ApiKeyPlaceholder = "%holerr-api-key-placeholder%"

func GetApiKey() string {
	return viper.GetString(ConfKeyApiKey)
}

func SetApiKey(apiKey string) {
	viper.Set(ConfKeyApiKey, apiKey)
	viper.WriteConfig()

	replacer := placeholder.Replacer{
		Placeholder: ApiKeyPlaceholder,
		Replacement: apiKey,
		IsURLPath: false,
	}
	placeholder.SetReplacer(replacer)

	placeholder.ReplaceInFiles(GetPublicDir())
}
