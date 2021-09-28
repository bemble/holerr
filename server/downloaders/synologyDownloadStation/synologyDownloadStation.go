package synologyDownloadStation

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
	"holerr/core/config"
	"holerr/core/db"
	"holerr/core/log"
	"holerr/downloaders/downloader"

	"github.com/monaco-io/request"
)

var cfg = config.Get()
var synoCfg = cfg.Downloaders.SynologyDownloadStation
var ENDPOINT = synoCfg.Endpoint

type SynologyDownloadStation struct {
	downloader.Downloader
}

func New() SynologyDownloadStation {
	s := SynologyDownloadStation{}
	sid, err := connect("DownloadStation")
	if err != nil {
		log.Fatal(err)
	}
	log.Info("DownloadStation session ID: " + sid)
	return s
}

func (r SynologyDownloadStation) IsConnected() bool {
	sid, err := connect("DownloadStation")
	return err == nil && sid != ""
}

func (s SynologyDownloadStation) AddDownload(uri string, name string, preset config.Preset) (string, error) {
	sid, err := connect("DownloadStation")
	if err != nil {
		log.Fatal(err)
	}

	req, err := http.NewRequest(http.MethodGet, getApiUrl("/DownloadStation/task.cgi"), nil)
	if err != nil {
		return "", err
	}

	q := req.URL.Query()
	q.Add("api", "SYNO.DownloadStation.Task")
	q.Add("version", "1")
	q.Add("method", "create")
	q.Add("uri", uri)
	q.Add("_sid", sid)

	destination := preset.OutputDir
	if destination != "" {
		if preset.CreateSubDir {
			err := createOutputDir(destination, name)
			if err != nil {
				return "", err
			}
			destination = destination + "/" + name
		}
		q.Add("destination", destination)
	}
	req.URL.RawQuery = q.Encode()

	statusCode, body, err := makeRequest(req)
	if err != nil {
		return "", err
	}
	if statusCode != 200 {
		return "", errors.New("Could not add download")
	}
	var obj Status
	jsonError := json.Unmarshal(body, &obj)
	if jsonError != nil {
		return "", jsonError
	}
	if !obj.Success {
		return "", errors.New("Error while adding download")
	}

	return getId(uri)
}

func (s SynologyDownloadStation) GetTaskStatus(id string) (int, int, error) {
	sid, err := connect("DownloadStation")
	if err != nil {
		log.Fatal(err)
	}
	client := request.Client{
		URL: "/DownloadStation/task.cgi",
		Params: map[string]string{
			"api":        "SYNO.DownloadStation.Task",
			"version":    "1",
			"method":     "getinfo",
			"additional": "transfer",
			"id":         id,
			"_sid":       sid,
		},
	}
	prepareClient(&client)
	resp, err := client.Do()
	if err != nil {
		return 0, 0, err
	}
	if resp.Code != 200 {
		return 0, 0, errors.New("Could retrieve download info")
	}

	var obj Tasks
	jsonError := json.Unmarshal(resp.Data, &obj)
	if jsonError != nil {
		return 0, 0, jsonError
	}
	if !obj.Success {
		return 0, 0, errors.New("Error while get download info")
	}

	downloaderStatusMapping := map[string]int{
		downloader.DownloadStatus["WAITING"]:       db.DownloadStatus["DOWNLOADER_DOWNLOADING"],
		downloader.DownloadStatus["DOWNLOADING"]:   db.DownloadStatus["DOWNLOADER_DOWNLOADING"],
		downloader.DownloadStatus["PAUSED"]:        db.DownloadStatus["DOWNLOADER_DOWNLOADING"],
		downloader.DownloadStatus["FINISHING"]:     db.DownloadStatus["DOWNLOADER_DOWNLOADING"],
		downloader.DownloadStatus["FINISHED"]:      db.DownloadStatus["DOWNLOADER_DOWNLOADED"],
		downloader.DownloadStatus["HASH_CHECKING"]: db.DownloadStatus["DOWNLOADER_DOWNLOADING"],
		downloader.DownloadStatus["SEEDING"]:       db.DownloadStatus["DOWNLOADER_DOWNLOADED"],
		downloader.DownloadStatus["EXTRACTING"]:    db.DownloadStatus["DOWNLOADER_DOWNLOADING"],
		downloader.DownloadStatus["ERROR"]:         db.DownloadStatus["ERROR_DOWNLOADER"],
	}
	return downloaderStatusMapping[obj.Data.Tasks[0].Status], obj.Data.Tasks[0].Additional.Transfer.SizeDownloaded, nil
}

func (s SynologyDownloadStation) DeleteDownload(id string) error {
	sid, err := connect("DownloadStation")
	if err != nil {
		log.Fatal(err)
	}

	client := request.Client{
		URL: "/DownloadStation/task.cgi",
		Params: map[string]string{
			"api":     "SYNO.DownloadStation.Task",
			"version": "1",
			"method":  "delete",
			"id":      id,
			"_sid":    sid,
		},
	}
	prepareClient(&client)
	resp, err := client.Do()
	if err != nil {
		return err
	}
	if resp.Code != 200 {
		return errors.New("Could not delete download task")
	}

	return nil
}

func prepareClient(client *request.Client) {
	client.URL = ENDPOINT + "/webapi" + client.URL

	if client.Method == "" {
		client.Method = "GET"
	}
}

func getApiUrl(path string) string {
	return ENDPOINT + "/webapi" + path
}

func connect(session string) (string, error) {
	req, err := http.NewRequest(http.MethodGet, getApiUrl("/auth.cgi"), nil)
	if err != nil {
		return "", err
	}

	q := url.Values{}
	q.Add("api", "SYNO.API.Auth")
	q.Add("version", "3")
	q.Add("method", "login")
	q.Add("session", session)
	q.Add("account", synoCfg.Username)
	q.Add("passwd", synoCfg.Password)
	q.Add("format", "sid")
	req.URL.RawQuery = q.Encode()

	statusCode, body, err := makeRequest(req)
	if err != nil {
		return "", err
	}

	if statusCode != 200 {
		return "", errors.New("Could not login to " + session)
	}

	var obj Auth
	jsonError := json.Unmarshal(body, &obj)
	if jsonError != nil {
		return "", jsonError
	}
	if !obj.Success {
		return "", errors.New("Error while login to " + session)
	}
	return obj.Data.Sid, nil
}

func makeRequest(req *http.Request) (int, []byte, error) {
	req.URL.RawQuery = strings.ReplaceAll(req.URL.RawQuery, "+", "%20")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return 0, []byte{}, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	return resp.StatusCode, body, err
}

func getId(uri string) (string, error) {
	sid, err := connect("DownloadStation")
	if err != nil {
		log.Fatal(err)
	}

	client := request.Client{
		URL: "/DownloadStation/task.cgi",
		Params: map[string]string{
			"api":        "SYNO.DownloadStation.Task",
			"version":    "1",
			"method":     "list",
			"additional": "detail",
			"_sid":       sid,
		},
	}
	prepareClient(&client)
	resp, err := client.Do()
	if err != nil {
		return "", err
	}
	if resp.Code != 200 {
		return "", errors.New("Could not list downloads")
	}
	var obj Tasks
	jsonError := json.Unmarshal(resp.Data, &obj)
	if jsonError != nil {
		return "", jsonError
	}
	if !obj.Success {
		return "", errors.New("Error while search download id")
	}

	for _, task := range obj.Data.Tasks {
		if task.Additional.Detail.Uri == uri {
			return task.Id, nil
		}
	}

	return "", errors.New("Download not found")
}


func createOutputDir(parent string, name string) error {
	sid, err := connect("FileStation")
	if err != nil {
		log.Fatal(err)
	}

	req, err := http.NewRequest(http.MethodGet, getApiUrl("/entry.cgi"), nil)
	if err != nil {
		return err
	}

	folder_path := parent
	if(folder_path[0] != '/') {
		folder_path = "/" + folder_path
	}

	q := req.URL.Query()
	q.Add("api", "SYNO.FileStation.CreateFolder")
	q.Add("version", "2")
	q.Add("method", "create")
	q.Add("folder_path", folder_path)
	q.Add("name", name)
	q.Add("_sid", sid)
	req.URL.RawQuery = q.Encode()

	statusCode, body, err := makeRequest(req)
	if err != nil {
		return err
	}
	if statusCode != 200 {
		return errors.New("Could not create sub folder")
	}
	var obj Status
	jsonError := json.Unmarshal(body, &obj)
	if jsonError != nil {
		return jsonError
	}
	if !obj.Success {
		return errors.New("Error while creating sub folder")
	}

	return nil
}
