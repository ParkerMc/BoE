package webserver

import (
	"encoding/json"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/ParkerMc/BoE/model"
	"github.com/ParkerMc/BoE/webserver/model"
	"github.com/Tomasen/realip"
	"github.com/gorilla/mux"
)

// InitUsers inits the user routes
func (webserver *WebServer) InitUsers() {
	webserver.Routes.User.HandleFunc("", webserver.userRegister).Methods("POST")
	webserver.Routes.User.HandleFunc("", webserver.userGetUsers).Methods("GET")
	webserver.Routes.User.HandleFunc("/login", webserver.userLogin).Methods("POST")
	webserver.Routes.User.HandleFunc("/{id}", webserver.userGetUser).Methods("GET")
	webserver.Routes.User.HandleFunc("/{id}/password", webserver.userSetPassword).Methods("PUT")
	webserver.Routes.User.HandleFunc("/{id}/role/{role}", webserver.userAddRole).Methods("PUT")
	webserver.Routes.User.HandleFunc("/{id}/role/{role}", webserver.userRemoveRole).Methods("DELETE")
}

func (webserver *WebServer) userAddRole(w http.ResponseWriter, r *http.Request) {
	user, webErr := webserver.requireLogin(r)
	if webErr != nil {
		webErr.Send(w)
		return
	}
	admin := false
	for _, role := range user.Roles {
		if role == "admin" {
			admin = true
		}
	}
	id := mux.Vars(r)["id"]
	role := mux.Vars(r)["role"]
	if id == "me" {
		id = user.ID.Hex()
	}

	if !admin {
		webservermodel.NewErrorMessage("No perm", http.StatusForbidden).Send(w)
		return
	}
	detailErr := webserver.data.Database.UserAddRole(id, role)
	if detailErr != nil {
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (webserver *WebServer) userGetUser(w http.ResponseWriter, r *http.Request) {
	user, webErr := webserver.requireLogin(r)
	if webErr != nil {
		webErr.Send(w)
		return
	}
	admin := false
	for _, role := range user.Roles {
		if role == "admin" {
			admin = true
		}
	}
	id := mux.Vars(r)["id"]
	if id == "me" {
		id = user.ID.Hex()
	}
	foundUser, detailErr := webserver.data.Database.UserFromID(id)
	if detailErr != nil {
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}

	var response webservermodel.Responce
	if admin || id == user.ID.Hex() {
		response = webservermodel.UserPrivateResponse{
			User: webservermodel.UserPrivateFromUser(foundUser),
		}
	} else {
		response = webservermodel.UserPublicResponse{
			User: webservermodel.UserPublicFromUser(foundUser),
		}
	}
	response.Send(w, http.StatusOK)
}

func (webserver *WebServer) userGetUsers(w http.ResponseWriter, r *http.Request) {
	user, webErr := webserver.requireLogin(r)
	if webErr != nil {
		webErr.Send(w)
		return
	}
	admin := false
	for _, role := range user.Roles {
		if role == "admin" {
			admin = true
		}
	}
	page := 0
	pageSize := 50
	sortType := model.SortUserName
	var err error
	r.ParseForm()
	if _, ok := r.Form["page"]; ok {
		if page, err = strconv.Atoi(strings.Join(r.Form["page"], "")); err != nil {
			webservermodel.NewErrorMessage("page must be an int", http.StatusBadRequest).Send(w)
			return
		}
	}
	if _, ok := r.Form["page_size"]; ok {
		if pageSize, err = strconv.Atoi(strings.Join(r.Form["page_size"], "")); err != nil {
			webservermodel.NewErrorMessage("page_size must be an int", http.StatusBadRequest).Send(w)
			return
		}
	}
	if _, ok := r.Form["sort"]; ok {
		sortType = model.SortTypeFromString(strings.Join(r.Form["sort"], ""))
		if sortType != model.SortID && sortType != model.SortName && sortType != model.SortUserName {
			webservermodel.NewErrorMessage("sort is not a valid sorting type", http.StatusBadRequest).Send(w)
			return
		}
	}
	foundUsers, detailErr := webserver.data.Database.UserGetUsers(page, pageSize, sortType)
	if detailErr != nil {
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}

	if admin {
		response := webservermodel.UsersPrivateResponse{
			Users: make([]webservermodel.UserPrivate, 0),
		}
		for _, foundUser := range foundUsers {
			response.Users = append(response.Users, webservermodel.UserPrivateFromUser(&foundUser))
		}
		response.Send(w, http.StatusOK)
	} else {
		response := webservermodel.UsersPublicResponse{
			Users: make([]webservermodel.UserPublic, 0),
		}
		for _, foundUser := range foundUsers {
			response.Users = append(response.Users, webservermodel.UserPublicFromUser(&foundUser))
		}
		response.Send(w, http.StatusOK)
	}
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
	user, token, detailErr := webserver.data.Database.UserLogin(userIn.UserIdentifier, userIn.Password, ip)
	if detailErr != nil {
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	response := webservermodel.UserLoginResponse{
		Token: token.Token,
		User:  webservermodel.UserPrivateFromUser(user),
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
	webErr := userIn.CheckData()
	if webErr != nil {
		webErr.Send(w)
		return
	}
	detailErr := webserver.data.Database.UserRegister(userIn.Username, userIn.Name, userIn.Password, userIn.Email)
	if detailErr != nil {
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}

	ip := realip.FromRequest(r)
	user, token, detailErr := webserver.data.Database.UserLogin(userIn.Username, userIn.Password, ip)
	if detailErr != nil {
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	response := webservermodel.UserLoginResponse{
		Token: token.Token,
		User:  webservermodel.UserPrivateFromUser(user),
	}
	response.Send(w, http.StatusOK)
}

func (webserver *WebServer) userRemoveRole(w http.ResponseWriter, r *http.Request) {
	user, webErr := webserver.requireLogin(r)
	if webErr != nil {
		webErr.Send(w)
		return
	}
	admin := false
	for _, role := range user.Roles {
		if role == "admin" {
			admin = true
		}
	}
	id := mux.Vars(r)["id"]
	role := mux.Vars(r)["role"]
	if id == "me" {
		id = user.ID.Hex()
	}

	if !admin {
		webservermodel.NewErrorMessage("No perm", http.StatusForbidden).Send(w)
		return
	}
	detailErr := webserver.data.Database.UserRemoveRole(id, role)
	if detailErr != nil {
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (webserver *WebServer) userSetPassword(w http.ResponseWriter, r *http.Request) {
	user, webErr := webserver.requireLogin(r)
	if webErr != nil {
		webErr.Send(w)
		return
	}
	admin := false
	for _, role := range user.Roles {
		if role == "admin" {
			admin = true
		}
	}
	changePasswordIn := webservermodel.UserChangePasswordInput{}
	err := json.NewDecoder(r.Body).Decode(&changePasswordIn)
	if err != nil {
		webservermodel.NewErrorWithMsg("Error decoding json: %s", err, http.StatusBadRequest).Send(w)
		return
	}
	id := mux.Vars(r)["id"]
	if id == "me" {
		id = user.ID.Hex()
	}
	if user.ID.Hex() != id {
		if !admin {
			webservermodel.NewErrorMessage("No perm", http.StatusForbidden).Send(w)
			return
		}
		detailErr := webserver.data.Database.UserSetPassword(id, changePasswordIn.NewPassword)
		if detailErr != nil {
			webservermodel.NewErrorFromError(detailErr).Send(w)
			return
		}
		w.WriteHeader(http.StatusNoContent)
	} else {
		if changePasswordIn.CurrentPassword == "" {
			webservermodel.NewErrorMessage("current_password must not be blank", http.StatusBadRequest).Send(w)
			return
		}
		correct, detailErr := webserver.data.Database.UserCheckPassword(id, changePasswordIn.CurrentPassword)
		if detailErr != nil {
			webservermodel.NewErrorFromError(detailErr).Send(w)
			return
		}
		if correct {
			detailErr = model.UserCheckPassword(changePasswordIn.NewPassword)
			if detailErr != nil {
				webservermodel.NewErrorFromError(detailErr).Send(w)
				return
			}
			detailErr = webserver.data.Database.UserSetPassword(id, changePasswordIn.NewPassword)
			if detailErr != nil {
				webservermodel.NewErrorFromError(detailErr).Send(w)
				return
			}
			w.WriteHeader(http.StatusNoContent)
		} else {
			webservermodel.NewErrorMessage("Password incorrect", http.StatusUnauthorized).Send(w)
			return
		}
	}
}

func (webserver *WebServer) requireLogin(r *http.Request) (*model.User, *webservermodel.Error) {
	token := r.Header.Get("X-User-Token")
	id := r.Header.Get("X-User-Id")
	if token == "" {
		return nil, webservermodel.NewErrorMessage("X-User-Token not defined.", http.StatusBadRequest)

	}
	if id == "" {
		return nil, webservermodel.NewErrorMessage("X-User-Id not defined.", http.StatusBadRequest)
	}
	user, detailErr := webserver.data.Database.UserFromID(id)
	if detailErr != nil {
		return nil, webservermodel.NewErrorFromError(detailErr)

	}
	for _, userToken := range user.Tokens {
		if userToken.Token == token {
			if userToken.Expiration.Before(time.Now()) {
				webserver.data.Database.UserPurgeExpiredTokens(user.ID.Hex())
			} else {
				return user, nil
			}
			break
		}
	}
	return nil, webservermodel.NewErrorMessage("Token not valid.", http.StatusUnauthorized)
}
