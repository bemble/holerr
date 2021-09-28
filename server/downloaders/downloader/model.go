package downloader

var DownloadStatus = map[string]string{
	"WAITING":             "waiting",
	"DOWNLOADING":         "downloading",
	"PAUSED":              "paused",
	"FINISHING":           "finishing",
	"FINISHED":            "finished",
	"HASH_CHECKING":       "hash_checking",
	"SEEDING":             "seeding",
	"FILEHOSTING_WAITING": "filehosting_waiting",
	"EXTRACTING":          "extracting",
	"ERROR":               "error",
}
