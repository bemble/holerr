module holerr

go 1.15

replace (
	holerr/api => ./api
	holerr/core => ./core
	holerr/core/config => ./core/config
	holerr/core/db => ./core/db
	holerr/core/log => ./core/log
	holerr/debriders => ./debriders
	holerr/debriders/debrider => ./debriders/debrider
	holerr/debriders/realdebrid => ./debriders/realdebrid
	holerr/downloaders => ./downloaders
	holerr/downloaders/downloader => ./downloaders/downloader
	holerr/downloaders/synologyDownloadStation => ./downloaders/synologyDownloadStation
	holerr/scheduler => ./scheduler
)

require (
	github.com/go-chi/chi v1.5.1
	github.com/jcelliott/lumber v0.0.0-20160324203708-dd349441af25 // indirect
	github.com/monaco-io/request v1.0.5 // indirect
	github.com/nanobox-io/golang-scribble v0.0.0-20190309225732-aa3e7c118975 // indirect
	github.com/spf13/viper v1.7.1 // indirect
	holerr/api v0.0.0-00010101000000-000000000000
	holerr/core/config v0.0.0-00010101000000-000000000000
	holerr/core/db v0.0.0-00010101000000-000000000000
	holerr/core/log v0.0.0-00010101000000-000000000000
	holerr/debriders v0.0.0-00010101000000-000000000000
	holerr/debriders/debrider v0.0.0-00010101000000-000000000000 // indirect
	holerr/debriders/realdebrid v0.0.0-00010101000000-000000000000 // indirect
	holerr/downloaders v0.0.0-00010101000000-000000000000
	holerr/downloaders/downloader v0.0.0-00010101000000-000000000000 // indirect
	holerr/downloaders/synologyDownloadStation v0.0.0-00010101000000-000000000000 // indirect
	holerr/scheduler v0.0.0-00010101000000-000000000000
)
