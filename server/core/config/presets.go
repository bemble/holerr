package config

import (
	"errors"
	"fmt"
	"github.com/imdario/mergo"
	"github.com/spf13/viper"
	"os"
	"path/filepath"
)

func GetPresets() ([]Preset, bool) {
	if viper.IsSet(ConfKeyPresets) {
		presets := []Preset{}
		err := viper.UnmarshalKey(ConfKeyPresets, &presets)
		if err == nil {
			return presets, false
		}
	}
	return []Preset{}, true
}

func GetPresetByPath(filePath string) (Preset, error) {
	torrentDir := filepath.Dir(filePath)
	presets, _ := GetPresets()
	dataDir := GetDataDir()
	for _, a := range presets {
		presetDir := filepath.Clean(fmt.Sprintf(`%s/../data/%s`, dataDir, a.WatchDir))
		if presetDir == torrentDir {
			return a, nil
		}
	}
	return Preset{}, errors.New("No preset found for path " + filePath)
}

func GetPresetByName(name string) (Preset, error) {
	presets, _ := GetPresets()
	for _, a := range presets {
		if a.Name == name {
			return a, nil
		}
	}
	return Preset{}, errors.New("No preset found for name " + name)
}

func AddPreset(preset Preset) error {
	_, err := GetPresetByName(preset.Name)
	if err == nil {
		return errors.New("Preset " + preset.Name + " already exists")
	}

	presets, _ := GetPresets()
	presets = append(presets, preset)
	viper.Set(ConfKeyPresets, presets)
	createPresetDirs()
	viper.WriteConfig()
	return nil
}

func UpdatePreset(name string, preset Preset) error {
	_, err := GetPresetByName(preset.Name)
	if err == nil {
		return errors.New("Preset " + name + " not found")
	}

	presets, _ := GetPresets()
	for i, a := range presets {
		if a.Name == name {
			mergo.Merge(&presets[i], preset, mergo.WithOverride)
		}
	}
	viper.Set(ConfKeyPresets, presets)
	createPresetDirs()
	viper.WriteConfig()
	return nil
}

func RemovePreset(name string) {
	presets, _ := GetPresets()
	index := -1
	for i, a := range presets {
		if a.Name == name {
			index = i
		}
	}

	if index >= 0 {
		presets = append(presets[:index], presets[index+1:]...)
		viper.Set(ConfKeyPresets, presets)
		viper.WriteConfig()
	}
}

func createPresetDirs() {
	presets, _ := GetPresets()
	dataDir := GetDataDir()
	for _, a := range presets {
		presetDir := filepath.Clean(fmt.Sprintf(`%s/../data/%s`, dataDir, a.WatchDir))
		os.MkdirAll(presetDir, os.ModePerm)
	}
}
