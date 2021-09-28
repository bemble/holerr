package debrider

var TorrentStatus = map[string]string{
	"MAGNET_ERROR":             "magnet_error",
	"MAGNET_CONVERSION":        "magnet_conversion",
	"WAITING_FILES_SELECTION": "waiting_files_selection",
	"QUEUED":                   "queued",
	"DOWNLOADING":              "downloading",
	"DOWNLOADED":               "downloaded",
	"ERROR":                    "error",
	"VIRUS":                    "virus",
	"COMPRESSING":              "compressing",
	"UPLOADING":                "uploading",
	"DEAD":                     "dead",
}

type File struct {
	Id       int    `json:"id"`
	Path     string `json:"path"` // Path to the file inside the torrent, starting with "/"
	Bytes    int    `json:"bytes"`
	Selected int    `json:"selected"` // 0 or 1
}

type TorrentInfo struct {
	Id       string   `json:"id"`
	Filename string   `json:"filename"`
	Bytes    int      `json:"bytes"`    // Size of selected files only
	Progress int      `json:"progress"` // Possible values: 0 to 100
	Status   string   `json:"status"`   // Current status of the torrent
	Files    []File   `json:"files"`
	Links    []string `json:"links"`
}
