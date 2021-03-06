import { Preset } from "./presets.type";

export type Configuration = {
    // API key used to communicate with the server [default: ""]
    api_key: string;
    // Set holerr in debug (default: false)
    debug: boolean;
    // Current app version
    app_version: string;
    // Wether holerr is running using docker or not
    is_in_docker: boolean;
    // If necessary, the base_path to fetch the front [optional, default: "/"] example: "/holerr"
    base_path: string;
    // Debriders, providers that will download the torrent
    debriders?: Debriders;
    // Downloaders, providers that will download the files downloaded by the debrider
    downloaders?: Downloaders;
    // Download presets
    presets?: Preset[];
};

export type Debriders = {
    real_debrid: RealDebrid
}

export type RealDebrid = {
    api_key: string
}

export type Downloaders = {
    synology_download_station: SynologyDownloadStation
};

export type SynologyDownloadStation = {
    endpoint: string,
    username: string,
    password: string
};