package webserver

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/ParkerMc/BoE/webserver/model"
	"github.com/Tomasen/realip"
)

// InitUsers inits the user routes
func (webserver *WebServer) InitUsers() {
	webserver.Routes.User.HandleFunc("", webserver.userRegister).Methods("POST")
	webserver.Routes.User.HandleFunc("/login", webserver.userLogin).Methods("POST")
}

func (webserver *WebServer) userLogin(w http.ResponseWriter, r *http.Request) {
	userIn := webservermodel.UserLoginInput{}
	err := json.NewDecoder(r.Body).Decode(&userIn)
	if err != nil {
		webservermodel.NewErrorWithMsg("Error decoding json: %s", err, http.StatusBadRequest).Send(w)
		return
	}

	if userIn.UserIdentifier == "" {
		webservermodel.NewErrorMessage("user_id must not be empty.", http.StatusBadRequest).Send(w)
		return
	}
	if userIn.Password == "" {
		webservermodel.NewErrorMessage("password must not be empty.", http.StatusBadRequest).Send(w)
		return
	}
	ip := realip.FromRequest(r)
	log.Print(ip)
	user, token, createError := webserver.data.Database.UserLogin(userIn.UserIdentifier, userIn.Password, ip)
	if createError != nil {
		webservermodel.NewErrorFromError(createError).Send(w)
		return
	}
	response := webservermodel.UserLoginResponse{
		Success: true,
		Token:   token.Token,
		User:    webservermodel.UserPrivateFromUser(user),
	}
	response.Send(w, http.StatusOK)

}

func (webserver *WebServer) userRegister(w http.ResponseWriter, r *http.Request) {
	userIn := webservermodel.UserRegisterInput{}
	err := json.NewDecoder(r.Body).Decode(&userIn)
	if err != nil {
		webservermodel.NewErrorWithMsg("Error decoding json: %s", err, http.StatusBadRequest).Send(w)
		return
	}
	checkDataError := userIn.CheckData()
	if err != nil {
		webservermodel.NewErrorFromError(checkDataError).Send(w)
		return
	}
	createError := webserver.data.Database.UserRegister(userIn.Username, userIn.Name, userIn.Password, userIn.Email)
	if createError != nil {
		webservermodel.NewErrorFromError(createError).Send(w)
		return
	}

	ip := realip.FromRequest(r)
	user, token, createError := webserver.data.Database.UserLogin(userIn.Username, userIn.Password, ip)
	if createError != nil {
		webservermodel.NewErrorFromError(createError).Send(w)
		return
	}
	response := webservermodel.UserLoginResponse{
		Success: true,
		Token:   token.Token,
		User:    webservermodel.UserPrivateFromUser(user),
	}
	response.Send(w, http.StatusOK)
}
