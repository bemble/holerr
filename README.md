# Holerr

> Torrent -> Real Debrid -> Downloader

## Running

### Docker

```bash
docker run -v "/local/data:/app/data" -p8781:8781 pierrecle/holerr:latest 
```

### Docker compose

```yml
  holerr:
    image: pierrecle/holerr:latest
    container_name: holerr
    restart: unless-stopped
    ports:
      - ${PORT_HOLERR}:8781
    volumes:
      - "${PWD}/holerr/data:/app/data"
      - /usr/share/zoneinfo:/usr/share/zoneinfo:ro
      - /etc/localtime:/etc/localtime:ro
```

## Configuration

Create a `config.json` file in the data directory.

```typescript
type Configuration = {
    // Set holerr in debug (default: false)
    debug: boolean,
    // If necessary, the base_path to fetch the front [optional, default: ""] example: "/holerr"
    base_path: string,
    // Debriders, providers that will download the torrent
    debriders: {
        // Real-Debrid
        real_debrid: {
            // Real-Debrid private API token: https://real-debrid.com/apitoken
            api_key: string
        }
    },
    // Downloaders, providers that will download the files downloaded by the debrider
    downloaders: {
        // Synology
        synology_download_station: {
            // Your Synology endpoint (example: "http://192.168.1.1:5000")
            endpoint: string,
            // DSM username (this user must not have 2FA)
            username: string,
            // DSM password
            password: string
        }
    },
    // Presets, see in Data structure
    presets: Preset[]
}
```

## Development

### Requirements

* Golang version 1.15 minimum must be installed

### Folder structure

* Create a `data` folder at project root

### Running the server

Server will run on port `8781`

```bash
cd server
go run main.go
```

### Front

A minimal web interface is given to monitor what happens. Open your browser and navigate to `http://localhost:8781`

## API documentation

### Websocket

A websocket connection will push events when concerned.

* __Endpoint:__ `/api/ws`
* __Protocol:__ `ws`

Example: `ws://192.168.1.1:8781/api/ws`

#### Messages

Messages are JSON objects stringified, with the following shape:

```typescript
type WebsocketInputMessage = {
    // Action to perform
    action: string,
    // Payload, if concerned
    payload?: any
}
```

##### Actions

* __`downloads/new`:__ new download found, payload is the new download
  ```typescript
  type WebsocketDownloadsNewInputMessage = {
    action: "downloads/new",
    payload: Download
  }
  ```
* __`downloads/update`:__ download has been updated, payload is the updated download
  ```typescript
  type WebsocketDownloadsUpdateInputMessage = {
    action: "downloads/update",
    payload: Download
  }
  ```
* __`downloads/delete`:__ download has been deleted, payload is the deleted download (also send
  on `/api/downloads/clean_up`)
  ```typescript
  type WebsocketDownloadsUpdateInputMessage = {
    action: "downloads/delete",
    payload: Download
  }
  ```

### HTTP

#### Constants

* __Get:__ `[GET] /api/status` get the status

#### Constants

* __List:__ `[GET] /api/constants` get the list of used constants

#### Presets

* __List:__ `[GET] /api/presets` get the list of presets (configured in `config.json`)

#### Downloads

* __List:__ `[GET] /api/downloads` get the list of downloads
* __Add:__ `[POST] /api/downloads` add a new torrent to holerr

  Data are sent using FormData.

  _Body structure:_
  ```typescript
  type PostTorrentBody = {
    // Preset name
    preset: string,
    // Torrent file
    torrent_file: File
  }
  ```
  _Example:_
  ```javascript
  const body = new FormData();
  body.append("preset", "Film");
  body.append("torrent_file", fileInput.files[0], "myFile.torrent");

  fetch("/api/downloads", {method: 'POST', body})
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
  ```
* __Delete:__ `[DELETE] /api/downloads/:id` abort the current download (torrent on debrider and download task on
  downloader will be deleted) and delete download from database
* __Clean:__ `[POST] /api/downloads/clean_up` remove downloads sent to downloader or in error from database

## Data structure

### Status

```typescript
type Status = {
    // Is connected to debrider
    debrider_connected: bool,
    // Is connected to downloader
    downloader_connected: bool
}
```

### Constants

```typescript
type Constants = {
    // Global download task status
    download_status: Record<string, number>,
    // Torrent status from debrider
    torrent_status: Record<string, number>
}
```

### Presets

```typescript
type Preset = {
    // Human readable name
    name: string,
    // Where holerr will watch torrents, relative to data dir
    watch_dir: string,
    // Downloader output directory [optional] (in Synology, must start with a shared folder)
    output_dir: string,
    // If true, create a sub directory, into output_dir, per download task and download files in it [optional, default: false]
    create_sub_dir: bool,
    // Accepted file extensions [optional]
    file_extensions: string[] | null,
    // Minimum file size to download [optional, default: 0]
    min_file_size: number
}
```

### Downloads

```typescript
type Download = {
    // Internal download id
    id: string;
    // Download title (computed from torrent file name)
    title: string;
    // Name of the preset used
    preset: string;
    // Global downlaod task status
    status: DownloadStatus;
    // Human readable status
    status_details: string;
    // Debrider torrent info (might have more data, according to the debrider used)
    torrent_info: TorrentInfo | null;
    // Downloader downloads info
    download_info: DownloadInfo | null;
    // Download task creation date
    created_at: string;
    // Download task last update date
    updated_at: string;
};

type TorrentInfo = {
    // Debrider torrent ID
    id: string,
    // Torrent filename
    filename: string,
    // Size of selected files only
    bytes: int,
    // Download progress [0...100]
    progress: int,
    // Current status of the torrent
    status: string,
    // List of file available in the torrent
    files: DownloadFile[],
    // When torrent is downloaded, list of files
    links: string[] | null
};

type DownloadFile = {
    // Debrider file ID
    id: int,
    // Path to the file inside the torrent, starting with "/"
    path: string,
    // Size of the file
    bytes: int,
    // Whether the file is selected for download or not [0,1]
    selected: int
};

type DownloadInfo = {
    // Download progress [0...100]
    progress: number;
    // Total files size
    bytes: number;
    // Key are links
    tasks: Record<string, DownloadInfoTask>
};

type DownloadInfoTask = {
    // Downloader ID
    id: string;
    // Tasks status
    status: number;
    // Downloaded
    bytes_downloaded: number;
};
```