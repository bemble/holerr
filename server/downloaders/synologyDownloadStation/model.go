package synologyDownloadStation

type AuthData struct {
	Sid string `json:"sid"`
}

type Auth struct {
	Status
	Data AuthData `json:"data"`
}

type Task struct {
	Id       string `json:"id"`
	Type     string `json:"type"`
	Username string `json:"username"`
	Title    string `json:"title"`
	Size     int    `json:"size"`
	Status   string `json:"status"`
	Additional TaskAdditional `json:"additional"`
}

type TaskAdditional struct {
	Detail   TaskDetail   `json:"detail"`
	File     []TaskFile   `json:"file"`
	Transfer TaskTransfer `json:"transfer"`
}

type TaskDetail struct {
	CreateTime  int    `json:"create_time"`
	Destination string `json:"destination"`
	Priority    string `json:"priority"`
	Uri         string `json:"uri"`
}

type TaskFile struct {
	Filename       string `json:"filename"`
	Priority       string `json:"priority"`
	Size           string `json:"size"`
	SizeDownloaded string `json:"size_downloaded"`
}

type TaskTransfer struct {
	DownloadedPieces int `json:"downloaded_pieces"`
	SizeDownloaded   int `json:"size_downloaded"`
	SizeUploaded     int `json:"size_uploaded"`
	SpeedDownload    int `json:"speed_download"`
	SpeedUpload      int `json:"speed_upload"`
}

type Tasks struct {
	Status
	Data TasksData `json:"data"`
}

type TasksData struct {
	Total  int    `json:"total"`
	Offset int    `json:"offset"`
	Tasks  []Task `json:"tasks"`
}

type Error struct {
	Code int `json:"code"`
}

type Status struct {
	Error   Error `json:"error"`
	Success bool  `json:"success"`
}
