package db

import (
	"time"
	"holerr/debriders/debrider"
)

var DownloadStatus = map[string]int{
	"TORRENT_FOUND":            0,
	"TORRENT_SENT_TO_DEBRIDER": 1,
	"DEBRIDER_DOWNLOADING":     2,
	"DEBRIDER_DOWNLOADED":      3,
	"SENT_TO_DOWNLOADER":       4,
	"DOWNLOADER_DOWNLOADING":   5,
	"DOWNLOADER_DOWNLOADED":    6,
	"ERROR_NO_FILES_FOUND":     100,
	"ERROR_DEBRIDER":           101,
	"ERROR_DOWNLOADER":         102,
}

var DownloadStatusDetail = map[int]string{
	DownloadStatus["TORRENT_FOUND"]:            "Torrent file found on drive",
	DownloadStatus["TORRENT_SENT_TO_DEBRIDER"]: "Torrent sent to debrider for download",
	DownloadStatus["DEBRIDER_DOWNLOADING"]:     "Debrider is downloading files, check on debrider",
	DownloadStatus["DEBRIDER_DOWNLOADED"]:      "Debrider download is terminated",
	DownloadStatus["SENT_TO_DOWNLOADER"]:       "Debrided files sent to downloader",
	DownloadStatus["DOWNLOADER_DOWNLOADING"]:   "Downloader is downloading the files",
	DownloadStatus["DOWNLOADER_DOWNLOADED"]:    "Downloader task is terminated",
	DownloadStatus["ERROR_NO_FILES_FOUND"]:     "No files found",
	DownloadStatus["ERROR_DEBRIDER"]:           "Debrider error",
	DownloadStatus["ERROR_DOWNLOADER"]:         "Downloader error",
}

type Download struct {
	Id            string               `json:"id"`
	Title         string               `json:"title"`
	Preset        string               `json:"preset"`
	Status        int                  `json:"status"`
	StatusDetails string               `json:"status_details"`
	TorrentInfo   debrider.TorrentInfo `json:"torrent_info"`
	DownloadInfo  DownloadInfo         `json:"download_info"`
	CreatedAt     time.Time            `json:"created_at"`
	UpdatedAt     time.Time            `json:"updated_at"`
}

type DownloadInfo struct {
	Progress int                         `json:"progress"`
	Bytes    int                         `json:"bytes"`
	Tasks    map[string]DownloadInfoTask `json:"tasks"`
}

type DownloadInfoTask struct {
	Id              string `json:"id"`
	Status          int    `json:"status"`
	BytesDownloaded int    `json:"bytes_downloaded"`
}
