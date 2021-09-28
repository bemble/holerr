package config

import (
	"errors"
	"fmt"
	"github.com/spf13/viper"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path"
	"path/filepath"
	"reflect"
	"runtime"
	"strings"
)

var c Config
const BASE_PATH_PLACEHOLDER = "%holerr-base-path-placeholder%"


func Get() *Config {
	if !isInited() {
		log.Println("Reading configuration")

		confFile := fmt.Sprintf(`%s/config.json`, GetDataDir())
		viper.SetConfigFile(confFile)

		viper.SetDefault("base_path", "")
		err := viper.ReadInConfig()
		if err != nil {
			panic(err)
		}

		unmarshalErr := viper.Unmarshal(&c)
		if unmarshalErr != nil {
			panic(unmarshalErr)
		}

		os.MkdirAll(GetPublicDir(), os.ModePerm)

		createPresetDirs()
		handleFrontBasePath()
	}
	return &c
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

func GetPresetByPath(filePath string) (Preset, error) {
	torrentDir := filepath.Dir(filePath)
	cfg := Get()
	dataDir := GetDataDir()
	for _, a := range cfg.Presets {
		presetDir := filepath.Clean(fmt.Sprintf(`%s/../data/%s`, dataDir, a.WatchDir))
		if presetDir == torrentDir {
			return a, nil
		}
	}
	return Preset{}, errors.New("No preset found for path " + filePath)
}

func GetPresetByName(name string) (Preset, error) {
	cfg := Get()
	for _, a := range cfg.Presets {
		if a.Name == name {
			return a, nil
		}
	}
	return Preset{}, errors.New("No preset found for name " + name)
}

func isInited() bool {
	return !reflect.DeepEqual(c, Config{})
}

func createPresetDirs() {
	cfg := Get()
	dataDir := GetDataDir()
	for _, a := range cfg.Presets {
		presetDir := filepath.Clean(fmt.Sprintf(`%s/../data/%s`, dataDir, a.WatchDir))
		os.MkdirAll(presetDir, os.ModePerm)
	}
}

func handleFrontBasePath() {
	cfg := Get()
	publicDir := GetPublicDir()
	err := filepath.Walk(publicDir,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if !info.IsDir() && !strings.HasSuffix(path, ".original") && containsBasePathPlaceHolder(path) {
				copy(path, path+".original")
			}
			return nil
		})
	if err != nil {
		log.Fatal(err)
	}

	basePath := cfg.BasePath
	if basePath == "" {
		basePath = "/"
	}
	err = filepath.Walk(publicDir,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if strings.HasSuffix(path, ".original") {
				err = replaceBasePathPlaceHolder(path, basePath)
				if err != nil {
					return err
				}
			}
			return nil
		})
	if err != nil {
		log.Fatal(err)
	}
}

func containsBasePathPlaceHolder(path string) bool {
	b, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}
	return strings.Contains(string(b), BASE_PATH_PLACEHOLDER)
}

func copy(src string, dst string) (int64, error) {
	source, err := os.Open(src)
	if err != nil {
		return 0, err
	}
	defer source.Close()

	destination, err := os.Create(dst)
	if err != nil {
		return 0, err
	}
	defer destination.Close()
	nBytes, err := io.Copy(destination, source)
	return nBytes, err
}

func replaceBasePathPlaceHolder(path string, basePath string) error {
	b, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}
	fullReplace := basePath + "/"
	if basePath == "/" {
		fullReplace = basePath
	}
	result := strings.Replace(string(b), "/" + BASE_PATH_PLACEHOLDER + "/", fullReplace, -1)
	result = strings.Replace(result, "/" + BASE_PATH_PLACEHOLDER , basePath, -1)

	outputPath := strings.TrimSuffix(path, ".original")
	destination, err := os.Create(outputPath)
	if err != nil {
		return err
	}
	defer destination.Close()
	destination.WriteString(result)
	return nil
}
