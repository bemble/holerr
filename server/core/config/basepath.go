package config

import (
	"github.com/spf13/viper"
	"holerr/core/tools/file"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

const BasePathPlaceholder = "%holerr-base-path-placeholder%"

func GetBasePath() string {
	return viper.GetString(ConfKeyBasePath)
}

func SetBasePath(base_path string) {
	viper.Set(ConfKeyBasePath, base_path)
	viper.WriteConfig()
	handleFrontBasePath()
}

func handleFrontBasePath() {
	publicDir := GetPublicDir()
	err := filepath.Walk(publicDir,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if !info.IsDir() && !strings.HasSuffix(path, ".original") && containsBasePathPlaceHolder(path) {
				file.Copy(path, path+".original")
			}
			return nil
		})
	if err != nil {
		log.Fatal(err)
	}

	basePath := GetBasePath()
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
	return strings.Contains(string(b), BasePathPlaceholder)
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
	result := strings.Replace(string(b), "/"+BasePathPlaceholder+"/", fullReplace, -1)
	result = strings.Replace(result, "/"+BasePathPlaceholder, basePath, -1)

	outputPath := strings.TrimSuffix(path, ".original")
	destination, err := os.Create(outputPath)
	if err != nil {
		return err
	}
	defer destination.Close()
	destination.WriteString(result)
	return nil
}
