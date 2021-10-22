package config

import (
	"fmt"
	"github.com/spf13/viper"
	"holerr/core/tools/placeholder"
	"log"
	"os"
	"path"
	"path/filepath"
	"runtime"
)

const ConfKeyApiKey = "api_key"
const ConfKeyBasePath = "base_path"
const ConfKeyDebriders = "debriders"
const ConfKeyDebug = "debug"
const ConfKeyDownloaders = "downloaders"
const ConfKeyPresets = "presets"

func InitFromFile() {
	log.Println("Reading configuration")

	confFile := fmt.Sprintf(`%s/config.json`, GetDataDir())
	_, err := os.Stat(confFile)
	if os.IsNotExist(err) {
		log.Println("Configuration file does not exists, creating an empty one")
		file, err := os.Create(confFile)
		if err != nil {
			log.Fatal(err)
		}
		file.WriteString("{}")
		defer file.Close()
	}

	viper.SetConfigFile(confFile)

	viper.SetDefault(ConfKeyBasePath, "/")

	err = viper.ReadInConfig()
	if err != nil {
		panic(err)
	}

	publicDir := GetPublicDir()
	os.MkdirAll(publicDir, os.ModePerm)

	basePathReplacer := placeholder.Replacer{
		Placeholder: BasePathPlaceholder,
		Replacement: GetBasePath(),
		IsURLPath: true,
	}
	placeholder.SetReplacer(basePathReplacer)

	apiKeyReplacer := placeholder.Replacer{
		Placeholder: ApiKeyPlaceholder,
		Replacement: GetApiKey(),
		IsURLPath: false,
	}
	placeholder.SetReplacer(apiKeyReplacer)

	placeholder.ReplaceInFiles(publicDir)

	createPresetDirs()
}

func GetServerDir() (string, error) {
	_, currentFilePath, _, _ := runtime.Caller(0)
	currentFileDir := path.Dir(currentFilePath)
	return filepath.Abs(fmt.Sprintf(`%s/../..`, currentFileDir))
}

func GetPublicDir() string {
	dir, _ := GetServerDir()
	return filepath.Clean(fmt.Sprintf(`%s/../public`, dir))
}

func GetDataDir() string {
	dir, _ := GetServerDir()
	return filepath.Clean(fmt.Sprintf(`%s/../data`, dir))
}
