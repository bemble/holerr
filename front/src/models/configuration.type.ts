import {Preset} from "./presets.type";

export type Configuration = {
    base_path: string,
    debug: boolean,
    debriders?: Debriders,
    downloaders?: Downloaders,
    presets?: Preset[]
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