package config

type Config struct {
	BasePath    string      `mapstructure:"base_path"`
	Debug       bool        `mapstructure:"debug"`
	Debriders   Debriders   `mapstructure:"debriders"`
	Downloaders Downloaders `mapstructure:"downloaders"`
	Presets     []Preset    `mapstructure:"presets"`
}

type Debriders struct {
	RealDebrid RealDebrid `mapstructure:"real_debrid"`
}

type RealDebrid struct {
	ApiKey string `mapstructure:"api_key"`
}

type Downloaders struct {
	SynologyDownloadStation SynologyDownloadStation `mapstructure:"synology_download_station"`
}

type SynologyDownloadStation struct {
	Endpoint string `mapstructure:"endpoint"`
	Username string `mapstructure:"username"`
	Password string `mapstructure:"password"`
}

type Preset struct {
	Name           string   `mapstructure:"name"json:"name"`
	WatchDir       string   `mapstructure:"watch_dir"json:"watch_dir"`
	OutputDir      string   `mapstructure:"output_dir"json:"output_dir"`
	CreateSubDir   bool     `mapstructure:"create_sub_dir"json:"create_sub_dir"`
	FileExtensions []string `mapstructure:"file_extensions"json:"file_extensions"`
	MinFileSize    int      `mapstructure:"min_file_size"json:"min_file_size"`
}
