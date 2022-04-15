package config

import "os"

func IsInDocker() bool {
	return os.Getenv("IS_IN_DOCKER") == "1"
}
