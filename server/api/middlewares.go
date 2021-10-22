package api

import (
	"encoding/json"
	"holerr/core/config"
	"net/http"
)

func CheckApiKey(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		apiKey := config.GetApiKey()

		if apiKey != "" {
			userApiKey := r.Header.Get("X-Api-Key")
			if userApiKey == "" {
				userApiKey = r.URL.Query().Get("x-api-key")
			}

			if userApiKey != apiKey {
				w.WriteHeader(http.StatusForbidden)
				content := map[string]string {
					"message" : "Forbidden",
				}
				body, _ := json.Marshal(content)
				w.Write(body)
				return
			}
		}

		next.ServeHTTP(w, r)
	})
}
