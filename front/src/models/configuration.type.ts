import { Preset } from "./presets.type";

export type Configuration = {
  // API key used to communicate with the server [default: ""]
  api_key: string;
  // Current app version
  app_version: string;
  // If necessary, the base_path to fetch the front [optional, default: "/"] example: "/holerr"
  base_path: string;
  // Debriders, providers that will download the torrent
  debrider?: Debrider;
  // Downloaders, providers that will download the files downloaded by the debrider
  downloader?: Downloader;
  // Download presets
  presets?: Preset[];
};

export type Debrider = {
  real_debrid: RealDebrid;
};

export type RealDebrid = {
  api_key: string;
};

export type Downloader = {
  synology_download_station: SynologyDownloadStation;
};

export type SynologyDownloadStation = {
  endpoint: string;
  username: string;
  password: string;
};
