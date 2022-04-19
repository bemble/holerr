package config

type Config struct {
	Debug       *bool       `mapstructure:"debug"json:"debug"`
	ApiKey      string      `mapstructure:"api_key"json:"api_key"`
	BasePath    string      `mapstructure:"base_path"json:"base_path"`
	Debriders   Debriders   `mapstructure:"debriders"json:"debriders"`
	Downloaders Downloaders `mapstructure:"downloaders"json:"downloaders"`
	Presets     []Preset    `mapstructure:"presets"json:"downloaders"`
}

type Debriders struct {
	RealDebrid RealDebrid `mapstructure:"real_debrid"json:"real_debrid"`
}

type RealDebrid struct {
	ApiKey string `mapstructure:"api_key"json:"api_key"`
}

type Downloaders struct {
	SynologyDownloadStation SynologyDownloadStation `mapstructure:"synology_download_station"json:"synology_download_station"`
}

type SynologyDownloadStation struct {
	Endpoint string `mapstructure:"endpoint"json:"endpoint"`
	Username string `mapstructure:"username"json:"username"`
	Password string `mapstructure:"password"json:"password"`
}

type Preset struct {
	Name           string   `mapstructure:"name"json:"name"`
	WatchDir       string   `mapstructure:"watch_dir"json:"watch_dir"`
	OutputDir      string   `mapstructure:"output_dir"json:"output_dir"`
	CreateSubDir   *bool    `mapstructure:"create_sub_dir"json:"create_sub_dir"`
	FileExtensions []string `mapstructure:"file_extensions"json:"file_extensions"`
	MinFileSize    *int     `mapstructure:"min_file_size"json:"min_file_size"`
}
