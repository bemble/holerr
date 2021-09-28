package realdebrid

import "holerr/debriders/debrider"

type Profile struct {
	Id         int    `json:"id"`
	Username   string `json:"username"`
	Email      string `json:"email"`
	Points     int    `json:"points"`
	Locale     string `json:"locale"`
	Avatar     string `json:"avatar"`
	Type       string `json:"type"`
	Premium    int    `json:"premium"`
	Expiration string `json:"expiration"`
}

type ActiveCount struct {
	Nb    int `json:"nb"`
	Limit int `json:"limit"`
}

type Torrent struct {
	Id  string `json:"id"`
	Uri string `json:"uri"`
}

type RealDebridTorrentInfo struct {
	debrider.TorrentInfo
	OriginalFilename string   `json:"original_filename"` // Original name of the torrent
	Hash             string   `json:"hash"`              // SHA1 Hash of the torrent
	OriginalBytes    int      `json:"original_bytes"`    // Total size of the torrent
	Host             string   `json:"host"`              // Host main domain
	Split            int      `json:"split"`             // Split size of links
	Added            string   `json:"added"`             // jsonDate
	Ended            string   `json:"ended"`   // !! Only present when finished, jsonDate
	Speed            int      `json:"speed"`   // !! Only present in "downloading", "compressing", "uploading" status
	Seeders          int      `json:"seeders"` // !! Only present in "downloading", "magnet_conversion" status
}
