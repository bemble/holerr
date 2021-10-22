package placeholder

import (
	"holerr/core/tools/file"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

var replacers map[string]Replacer = map[string]Replacer{}

func SetReplacer(replacer Replacer) {
	replacers[replacer.Placeholder] = replacer
}

func ReplaceInFiles(rootDirectory string) {
	err := filepath.Walk(rootDirectory,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if !info.IsDir() && !strings.HasSuffix(path, ".original") && containsPlaceHolders(path) {
				file.Copy(path, path+".original")
			}
			return nil
		})
	if err != nil {
		log.Fatal(err)
	}

	err = filepath.Walk(rootDirectory,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if strings.HasSuffix(path, ".original") {
				err = replacePlaceHolders(path)
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

func containsPlaceHolders(path string) bool {
	b, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}
	contains := false
	for _, replacer := range replacers {
		contains = contains || strings.Contains(string(b), replacer.Placeholder)
	}

	return contains
}

func replacePlaceHolders(path string) error {
	b, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}

	result := string(b)

	for _, replacer := range replacers {
		fullReplace := replacer.Replacement
		if replacer.IsURLPath && replacer.Replacement != "/" {
			fullReplace = replacer.Replacement + "/"
		}

		if replacer.IsURLPath {
			result = strings.Replace(result, "/"+replacer.Placeholder+"/", fullReplace, -1)
			result = strings.Replace(result, "/"+replacer.Placeholder, replacer.Replacement, -1)
		} else {
			result = strings.Replace(result, replacer.Placeholder, replacer.Replacement, -1)
		}
	}

	outputPath := strings.TrimSuffix(path, ".original")
	destination, err := os.Create(outputPath)
	if err != nil {
		return err
	}
	defer destination.Close()
	destination.WriteString(result)
	return nil
}
