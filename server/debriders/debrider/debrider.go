package debrider

type Debrider interface {
	GetName() string
	IsConnected() bool
	Me() (string, error)
	GetSlotsAvailable() (int, error)
	GetActiveDownloads()
	AddTorrent(torrent string) (string, error)
	GetTorrentInfos(torrentId string) (TorrentInfo, error)
	SelectFiles(torrentId string, files []string) error
	DeleteTorrent(torrentId string) error
}
