# bemble/holerr

[![gh_last_release_svg]][gh_last_release_url]
[![tippin_svg]][tippin_url]

[gh_last_release_svg]: https://img.shields.io/github/v/release/bemble/holerr?sort=semver
[gh_last_release_url]: https://github.com/bemble/holerr/releases/latest
[tippin_svg]: https://img.shields.io/badge/donate-BuyMeACoffee-ffdd00?logo=buymeacoffee&style=flat
[tippin_url]: https://www.buymeacoffee.com/bemble

> Torrent & magnet -> Debrider -> Downloader

## Running

### Docker

```bash
docker run -v "/local/data:/app/data" -p8765:8765 ghcr.io/bemble/holerr:latest
```

### Docker compose

```yml
holerr:
  image: ghcr.io/bemble/holerr:latest
  container_name: holerr
  restart: unless-stopped
  ports:
    - ${PORT_HOLERR}:8765
  volumes:
    - "${PWD}/holerr/data:/app/data"
    - /usr/share/zoneinfo:/usr/share/zoneinfo:ro
    - /etc/localtime:/etc/localtime:ro
```

## Supported debriders & downloaders

**Debriders:**

- Real-Debrid

**Downloaders:**

- Synology Download Station

## Migrate from v1

The main file to migrate is the configuration, but holerr will migrate your configuration file from v1 to v2 after its first starts.
:warning: Also note that default port has changed, it's now `8765`

## Configuration

Create a `config.yaml` file in the data directory.

```yaml
# Select the logger to set in debug
debug: # optional, string[]
  - holerr.*
# If necessary, project base path (root path), when run behind a proxy fo example
base_path: /holerr # optional, string
# Debrider configuration
debrider:
  real_debrid:
    # Real-Debrid private API token: https://real-debrid.com/apitoken
    api_key: your key # string
# Downloader configuration
downloader:
  # Synology
  synology_download_station:
    # Your Synology endpoint
    endpoint: synology endpoint # string (example: "http://192.168.1.1:5000")
    # DSM username (this user must not have 2FA)
    username: dsm user # string
    # DSM password
    password: use password # string
  # Aria2
  aria2_jsonrpc:
    # Your aria2 JSON-RPC endpoint (http)
    endpoint: aria2 endpoint # string (example: "http://192.168.1.1:6000")
    # Aria2 JSONRPC secret
    secret: aria2 secret # optional, string
# Presets list
presets:
  - name: Downloads # string
    # Directory that holerr will watch
    watch_dir: holes/downloads # string
    # Downloader output directory, relative to the downloader
    output_dir: Downloads # string
    # Whether the file should be downloaded in a subdoctory or not
    create_sub_dir: false # optional, boolean
    # Restrict the extensions to download, default no-restriction
    file_extensions: # optional, string[]
    # Restrict the size of the files to download, default no restriction
    min_file_size: # human readbale string, example: 3.0B, 12KB, 432.2MB, 4.5GB, 1TB
```

:warning: currently, you can only have one debrider and one downloader.

### Synology specifics

You should have a user dedicated to this. Create a user (_Configuration_ > _Users and groups_), for this project it only needs access to DownloadStation application and write/read access to the output directories.

User **must** not have two factor authentication enabled, API calls won't work otherwise.

Before being able to start a download in Download Station you **must**:

- allow access to DSM (_Configuration_ > _Users and groups_ > _[the user], edit_ > _Applications_ > _DSM_)
- log in once in DSM
- open Download Station in this user session once to select the default output directory
- log out
- remove access to DSM for this user (_Configuration_ > _Users and groups_ > _[the user], edit_ > _Applications_ > _DSM_)

### Aria2 specifics

aria2 does not push any progress event over websocket, it has to be pulled, so for now there's real advantage to implement websocket connection.

## Development

### Folder structure

- Create a `data` folder at project root
- Add a configuration file
- :warning: while developing, you should not use a `base_path`

### Prepare environment

#### Front

```bash
cd front
npm i
```

#### Server

Create a virtual environment:

- In VSCode, open command palette (`Shift+CMD+P`) > `Python: Create Environment...`
- Select `Venv`
- Select `server` workspace
- Check `requirements.txt`

### Running the front and the server

Open VS Code, start the dev container. There's 2 tasks:

- Run front
- Run server

Database migrations will be run before the server starts.

## API documentation

Simply navigate to http://localhost:8765/docs or http://localhost:8765/redoc.
