package realdebrid

import (
	"encoding/json"
	"errors"
	"github.com/monaco-io/request"
	"holerr/core/config"
	"holerr/debriders/debrider"
	"io/ioutil"
	"net/url"
	"strings"
)

const ENDPOINT = "https://api.real-debrid.com/rest/1.0"
const MAXIMUM_ACTIVE_DOWNLOADS = 20

type RealDebrid struct {
	debrider.Debrider
}

func New() RealDebrid {
	return RealDebrid{}
}

func prepareClient(client *request.Client) {
	client.URL = ENDPOINT + client.URL

	if client.Method == "" {
		client.Method = "GET"
	}

	if client.Header == nil {
		client.Header = map[string]string{}
	}

	if client.Header["Authorization"] == "" {
		realDebridConf, _ := config.GetRealDebrid()
		client.Header["Authorization"] = "Bearer " + realDebridConf.ApiKey
	}
}

func (r RealDebrid) GetName() string {
	return "Real-Debrid"
}

func (r RealDebrid) IsConnected() bool {
	me, err := r.Me()
	return err == nil && me != ""
}

func (r RealDebrid) Me() (string, error) {
	client := request.Client{
		URL: "/user",
	}
	prepareClient(&client)
	resp, err := client.Do()
	if err != nil || resp.Code != 200 {
		return "", err
	}
	var obj Profile
	jsonError := json.Unmarshal(resp.Data, &obj)
	return obj.Username, jsonError
}

func (r RealDebrid) GetSlotsAvailable() (int, error) {
	client := request.Client{
		URL: "/torrents/activeCount",
	}
	prepareClient(&client)
	resp, err := client.Do()
	if err != nil || resp.Code != 200 {
		return 0, err
	}
	var obj ActiveCount
	jsonError := json.Unmarshal(resp.Data, &obj)
	return MAXIMUM_ACTIVE_DOWNLOADS - obj.Nb, jsonError
}

func (r RealDebrid) GetActiveDownloads() {
	// TODO: get active downloads
}

func (r RealDebrid) AddTorrent(torrent string) (string, error) {
	content, err := ioutil.ReadFile(torrent)
	if err != nil {
		return "", err
	}
	client := request.Client{
		URL:    "/torrents/addTorrent",
		Method: "PUT",
		Body:   content,
	}
	prepareClient(&client)
	resp, err := client.Do()
	if err != nil || resp.Code != 201 {
		return "", err
	}
	var obj Torrent
	jsonError := json.Unmarshal(resp.Data, &obj)
	return obj.Id, jsonError
}

func (r RealDebrid) GetTorrentInfos(torrentId string) (debrider.TorrentInfo, error) {
	client := request.Client{
		URL: "/torrents/info/" + torrentId,
	}
	prepareClient(&client)
	resp, err := client.Do()
	if err != nil {
		return debrider.TorrentInfo{}, err
	}
	if resp.Code != 200 {
		return debrider.TorrentInfo{}, errors.New("Error while getting torrent info")
	}
	var obj debrider.TorrentInfo
	jsonError := json.Unmarshal(resp.Data, &obj)
	return obj, jsonError
}

func (r RealDebrid) SelectFiles(torrentId string, files []string) error {
	data := url.Values{}
	data.Set("files", strings.Join(files, ","))
	client := request.Client{
		URL:         "/torrents/selectFiles/" + torrentId,
		Method:      "POST",
		ContentType: request.ApplicationXWwwFormURLEncoded,
		Body:        []byte(data.Encode()),
	}
	prepareClient(&client)
	_, err := client.Do()
	return err
}

func (r RealDebrid) DeleteTorrent(torrentId string) error {
	client := request.Client{
		URL:    "/torrents/delete/" + torrentId,
		Method: "DELETE",
	}
	prepareClient(&client)
	_, err := client.Do()
	return err
}
