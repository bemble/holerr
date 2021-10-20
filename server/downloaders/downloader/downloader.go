package downloader

import "holerr/core/config"

type Downloader interface {
	GetName() string
	IsConnected() bool
	AddDownload(uri string, name string, preset config.Preset) (string, error)
	GetTaskStatus(id string) (int, int, error) // Status, SizeDownloaded, error
	DeleteDownload(id string) error
}
