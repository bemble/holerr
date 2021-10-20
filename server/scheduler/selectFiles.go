package scheduler

import (
	"fmt"
	"holerr/core/config"
	"holerr/core/db"
	"holerr/core/log"
	"holerr/debriders"
	"strings"
)

func SelectFiles(download *db.Download) {
	debrider := debriders.Get()
	if debrider != nil {
		log.Info("No debrider set")
	}

	if download.Preset != "" && len(download.TorrentInfo.Files) >= 1 {
		preset, err := config.GetPresetByName(download.Preset)
		if err != nil {
			log.Error(err)
			return
		}

		filesExtensionFiltred := []string{}
		if len(preset.FileExtensions) > 0 {
			for _, file := range download.TorrentInfo.Files {
				for _, ext := range preset.FileExtensions {
					if strings.HasSuffix(file.Path, ext) {
						filesExtensionFiltred = append(filesExtensionFiltred, fmt.Sprintf("%d", file.Id))
					}
					break
				}
			}
		} else {
			for _, file := range download.TorrentInfo.Files {
				filesExtensionFiltred = append(filesExtensionFiltred, fmt.Sprintf("%d", file.Id))
			}
		}

		filesMinSizeFiltred := []string{}
		if preset.MinFileSize > 0 {
			for _, file := range download.TorrentInfo.Files {
				if file.Bytes >= preset.MinFileSize {
					filesMinSizeFiltred = append(filesMinSizeFiltred, fmt.Sprintf("%d", file.Id))
				}
			}
		} else {
			for _, file := range download.TorrentInfo.Files {
				filesMinSizeFiltred = append(filesMinSizeFiltred, fmt.Sprintf("%d", file.Id))
			}
		}

		files := intersect(filesExtensionFiltred, filesMinSizeFiltred)
		if len(files) == 0 {
			// TODO: delete torrent
			log.Info("No file selected for " + download.Title)
		}

		err = debrider.SelectFiles(download.TorrentInfo.Id, files)
		if err != nil {
			log.Error(err)
		}
		UpdateDebriderInfos(download)
	}
}

func intersect(s1 []string, s2 []string) []string {
	res := []string{}
	for _, a := range s1 {
		if contains(s2, a) {
			res = append(res, a)
		}
	}
	return res
}

func contains(s []string, e string) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}
