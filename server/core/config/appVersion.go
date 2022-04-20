package config

import "os"

func AppVersion() string {
	if os.Getenv("APP_VERSION") == "" {
		return "local"
	}
	return os.Getenv("APP_VERSION")
}
