export type Preset = {
  // Human readable name
  name: string;
  // Where holerr will watch torrents, relative to data dir
  watch_dir: string;
  // Downloader output directory [optional] (in Synology, must start with a shared folder)
  output_dir: string;
  // Accepted file extensions [optional]
  file_extensions: string[] | null;
  // Minimum file size to download [optional, default: 0]
  min_file_size: string | null;
  // Whether downloader should download in subdir
  create_sub_dir?: boolean;
};
