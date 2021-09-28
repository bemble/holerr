package api

import (
	"encoding/json"
	"github.com/gorilla/websocket"
	"net/http"
	"sync"
	"holerr/core/log"
)

var connectionPool = struct {
	sync.RWMutex
	connections map[*websocket.Conn]struct{}
}{
	connections: make(map[*websocket.Conn]struct{}),
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

func Websocket(w http.ResponseWriter, req *http.Request) {
	upgrader.CheckOrigin = func(r *http.Request) bool { return true }
	con, err := upgrader.Upgrade(w, req, nil)
	if err != nil {
		log.Error(err)
	}
	connectionPool.Lock()
	connectionPool.connections[con] = struct{}{}
	connectionPool.Unlock()
}

func WebsocketBroadcast(action string, payload interface{}) {
	message, _ := json.Marshal(map[string]interface{}{
		"action":  action,
		"payload": payload,
	})

	connectionPool.Lock()
	defer connectionPool.Unlock()
	for connection := range connectionPool.connections {
		if err := connection.WriteMessage(websocket.TextMessage, message); err != nil {
			delete(connectionPool.connections, connection)
			log.Error(err)
		}
	}
}

func contains(s []*websocket.Conn, e *websocket.Conn) bool {
	for _, ws := range s {
		if ws == e {
			return true
		}
	}
	return false
}
