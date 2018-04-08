package webserver

import (
	"log"
	"net/http"

	"github.com/ParkerMc/BoE/data"
	"github.com/ParkerMc/BoE/utils"
	"github.com/gorilla/mux"
)

const apiVersion string = "x"

// WebServer stores everything needed for the web server to activate
type WebServer struct {
	server *http.Server
	data   *data.Data
	Routes Routes
}

// Routes subtype of WebServer it stores all the routes
type Routes struct {
	Root *mux.Router
	API  *mux.Router
	User *mux.Router
}

// Init inits the web server
func Init(data *data.Data) *WebServer {
	webserver := &WebServer{data: data, Routes: Routes{}}

	webserver.Routes.Root = mux.NewRouter()
	webserver.Routes.API = webserver.Routes.Root.PathPrefix("/api/v" + apiVersion).Subrouter()
	webserver.Routes.User = webserver.Routes.API.PathPrefix("/users").Subrouter()

	webserver.InitClient()
	webserver.InitUsers()

	webserver.server = &http.Server{Addr: data.Config.Address, Handler: webserver.Routes.Root}
	return webserver
}

// Start starts the web server
func (webserver *WebServer) Start() {
	log.Print("Web server started.")
	go func() {
		err := webserver.server.ListenAndServe()
		utils.CheckErrorFatal("Web server error: %s", err)
	}()
}

// Stop stops the web server
func (webserver *WebServer) Stop() {
	webserver.server.Close()
}
