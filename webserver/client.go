package webserver

import (
	"net/http"
)

// InitClient inits all the routes needed for the client
func (webserver *WebServer) InitClient() {
	webserver.Routes.Root.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("./client/static")))).Methods("GET")
	webserver.Routes.Root.HandleFunc("/", displayLogin).Methods("GET")
	webserver.Routes.Root.HandleFunc("/login", displayLogin).Methods("GET")
	webserver.Routes.Root.HandleFunc("/register", displayLogin).Methods("GET")
	webserver.Routes.Root.HandleFunc("/channel/{id}", displayLogin).Methods("GET")
}

func displayLogin(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "./client/index.html")
}
