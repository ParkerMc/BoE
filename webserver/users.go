package webserver

import (
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
	_, admin, requestedUser, webErr := webserver.userGetUserSubType(r) // Require login and get user requested
	if webErr != nil {                                                 // If there is an error send it
		webErr.Send(w)
		return
	}
	role := mux.Vars(r)["role"] // get the role

	if !admin { // If the user is not an admin return no perm error
		webservermodel.NewErrorMessage("No perm", http.StatusForbidden).Send(w)
		return
	}
	detailErr := webserver.data.Database.UserAddRole(requestedUser.ID.Hex(), role) // Add the role to the user
	if detailErr != nil {                                                          // If there is an error send it
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	w.WriteHeader(http.StatusNoContent) // Else if everything is successful return no content
}

func (webserver *WebServer) userGetUser(w http.ResponseWriter, r *http.Request) {
	user, admin, requestedUser, webErr := webserver.userGetUserSubType(r) // Require login and get user requested
	if webErr != nil {                                                    // If there is an error then send it
		webErr.Send(w)
		return
	}
	var response webservermodel.Responce      // Create responce
	if admin || requestedUser.ID == user.ID { // If they are an admin or the user requested
		response = webservermodel.UserPrivateResponse{ // create UserPrivate responce
			User: webservermodel.UserPrivateFromUser(requestedUser),
		}
	} else { // Else create a UserPublic responce
		response = webservermodel.UserPublicResponse{
			User: webservermodel.UserPublicFromUser(requestedUser),
		}
	}
	response.Send(w, http.StatusOK) // Send the responce with status ok
}

func userGetUsersPhraseData(r *http.Request) (int, int, model.SortType, *webservermodel.Error) {
	page := 0 // Set the defaults
	pageSize := 50
	sortType := model.SortUserName
	var err error
	r.ParseForm()                    // Parse the forms
	if _, ok := r.Form["page"]; ok { // If there is the page key
		if page, err = strconv.Atoi(strings.Join(r.Form["page"], "")); err != nil { // Get an int from it or error
			return 0, 0, model.SortNone, webservermodel.NewErrorMessage("page must be an int", http.StatusBadRequest)
		}
	}
	if _, ok := r.Form["page_size"]; ok { // If there is the page_size key
		if pageSize, err = strconv.Atoi(strings.Join(r.Form["page_size"], "")); err != nil { // Get an int from it or error
			return 0, 0, model.SortNone, webservermodel.NewErrorMessage("page_size must be an int", http.StatusBadRequest)
		}
	}
	if _, ok := r.Form["sort"]; ok { // If there is the sort key
		sortType = model.SortTypeFromString(strings.Join(r.Form["sort"], ""))                         // Get a sortType from it
		if sortType != model.SortID && sortType != model.SortName && sortType != model.SortUserName { // If it is not an aproved sort type then return with error
			return 0, 0, model.SortNone, webservermodel.NewErrorMessage("sort is not a valid sorting type", http.StatusBadRequest)
		}
	}
	return page, pageSize, sortType, nil // Return with all data
}

func (webserver *WebServer) userGetUsers(w http.ResponseWriter, r *http.Request) {
	_, admin, webErr := webserver.requireLogin(r) // Require login
	if webErr != nil {                            // If there is an error send it
		webErr.Send(w)
		return
	}
	page, pageSize, sortType, webErr := userGetUsersPhraseData(r)                           // Get all the data
	foundUsers, detailErr := webserver.data.Database.UserGetUsers(page, pageSize, sortType) // Get the user list
	if detailErr != nil {                                                                   // if there is an error send it
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}

	if admin { // If they are admin then give them the private responce
		response := webservermodel.UsersPrivateResponse{ // Create the responce
			Users: make([]webservermodel.UserPrivate, 0),
		}
		for _, foundUser := range foundUsers { // Add the users
			response.Users = append(response.Users, webservermodel.UserPrivateFromUser(&foundUser))
		}
		response.Send(w, http.StatusOK) // Send the responce
	} else {
		response := webservermodel.UsersPublicResponse{ // Create the response
			Users: make([]webservermodel.UserPublic, 0),
		}
		for _, foundUser := range foundUsers { // Add the users
			response.Users = append(response.Users, webservermodel.UserPublicFromUser(&foundUser))
		}
		response.Send(w, http.StatusOK) // Send the responce
	}
}

func (webserver *WebServer) userGetUserSubType(r *http.Request) (*model.User, bool, *model.User, *webservermodel.Error) {
	user, admin, webErr := webserver.requireLogin(r) // Require login
	if webErr != nil {                               // If there is an error return it
		return nil, false, nil, webErr
	}
	id := mux.Vars(r)["id"] // Get the Id
	if id == "me" {         // If the id is me replace it with the user id
		id = user.ID.Hex()
	}
	requestedUser, detailErr := webserver.data.Database.UserGetByID(id) // Get the user requested
	if detailErr != nil {                                               // If there is an error return it
		return nil, false, nil, webservermodel.NewErrorFromError(detailErr)

	}
	return user, admin, requestedUser, nil // Return all the values
}

func (webserver *WebServer) userLogin(w http.ResponseWriter, r *http.Request) {
	userIn, webErr := webservermodel.UserLoginInputFromJSON(r.Body) // Get the login object
	if webErr != nil {                                              // If there an error send it
		webErr.Send(w)
		return
	}
	ip := realip.FromRequest(r)                                                                             // TODO rewrite in own code later to prevent spoofing
	user, token, detailErr := webserver.data.Database.UserLogin(userIn.UserIdentifier, userIn.Password, ip) // Login as user
	if detailErr != nil {                                                                                   // If there is an error send it
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	response := webservermodel.UserLoginResponse{ // Create the responce
		Token: token.Token,
		User:  webservermodel.UserPrivateFromUser(user),
	}
	response.Send(w, http.StatusOK) // Send the responce
}

func (webserver *WebServer) userRegister(w http.ResponseWriter, r *http.Request) {
	userIn, webErr := webservermodel.UserRegisterInputFromJSON(r.Body) // Get the user object from json
	if webErr != nil {                                                 // If there is an error send it
		webErr.Send(w)
		return
	}
	// Register the user
	detailErr := webserver.data.Database.UserRegister(userIn.Username, userIn.Name, userIn.Password, userIn.Email)
	if detailErr != nil { // If there is an error send it
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}

	ip := realip.FromRequest(r) // Get the ip and login
	user, token, detailErr := webserver.data.Database.UserLogin(userIn.Username, userIn.Password, ip)
	if detailErr != nil { // If there is an error send it
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	response := webservermodel.UserLoginResponse{ // Fourm the responce
		Token: token.Token,
		User:  webservermodel.UserPrivateFromUser(user),
	}
	response.Send(w, http.StatusOK) // Send the responce
}

func (webserver *WebServer) userRemoveRole(w http.ResponseWriter, r *http.Request) {
	_, admin, requestedUser, webErr := webserver.userGetUserSubType(r) // Require login and get user requested
	if webErr != nil {                                                 // If there is an error send it
		webErr.Send(w)
		return
	}
	role := mux.Vars(r)["role"] // get the role

	if !admin { // If the user is not an admin return no perm error
		webservermodel.NewErrorMessage("No perm", http.StatusForbidden).Send(w)
		return
	}
	detailErr := webserver.data.Database.UserRemoveRole(requestedUser.ID.Hex(), role) // Remove the role to the user
	if detailErr != nil {                                                             // If there is an error send it
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	w.WriteHeader(http.StatusNoContent) // Else if everything is successful return no content
}

func (webserver *WebServer) userSetPassword(w http.ResponseWriter, r *http.Request) {
	user, admin, requestedUser, webErr := webserver.userGetUserSubType(r) // Require login and get user requested
	if webErr != nil {                                                    // If there is an error then send it
		webErr.Send(w)
		return
	}
	changePasswordIn, webErr := webservermodel.UserChangePasswordInputFromJSON(r.Body) // Get the password change object
	if webErr != nil {                                                                 // If there is an error then send it
		webErr.Send(w)
		return
	}
	if user.ID != requestedUser.ID { // If the user is not changeing their own password
		if !admin { // And they are not admin then send the error
			webservermodel.NewErrorMessage("No perm", http.StatusForbidden).Send(w)
			return
		}
	} else { // Else the user is changing their own passowrd
		if changePasswordIn.CurrentPassword == "" { // If there is no current password send error
			webservermodel.NewErrorMessage("current_password must not be blank", http.StatusBadRequest).Send(w)
			return
		}
		// Check if the passowrord is correct
		correct, detailErr := webserver.data.Database.UserCheckPassword(requestedUser.ID.Hex(), changePasswordIn.CurrentPassword)
		if detailErr != nil { // If there is an error send it
			webservermodel.NewErrorFromError(detailErr).Send(w)
			return
		}
		if correct { // If the passoword is correct
			detailErr = model.UserCheckPassword(changePasswordIn.NewPassword) // Make sure that the new password matchs the requirements
			if detailErr != nil {                                             // If not send error
				webservermodel.NewErrorFromError(detailErr).Send(w)
				return
			}
		} else { // Else the password is incorrect send error
			webservermodel.NewErrorMessage("Password incorrect", http.StatusUnauthorized).Send(w)
			return
		}
	}
	// Set the password
	detailErr := webserver.data.Database.UserSetPassword(requestedUser.ID.Hex(), changePasswordIn.NewPassword)
	if detailErr != nil { // If there is an error send it
		webservermodel.NewErrorFromError(detailErr).Send(w)
		return
	}
	w.WriteHeader(http.StatusNoContent) // If there has been no error return with no content status code
}

func (webserver *WebServer) requireLogin(r *http.Request) (*model.User, bool, *webservermodel.Error) {
	token := r.Header.Get("X-User-Token")
	id := r.Header.Get("X-User-Id")
	if token == "" { // If the token is blank send error
		return nil, false, webservermodel.NewErrorMessage("X-User-Token not defined.", http.StatusBadRequest)
	}
	if id == "" { // If the id is blank send error
		return nil, false, webservermodel.NewErrorMessage("X-User-Id not defined.", http.StatusBadRequest)
	}
	user, detailErr := webserver.data.Database.UserGetByID(id) // Get the user by id
	if detailErr != nil {                                      // If there is an error return it and exit
		return nil, false, webservermodel.NewErrorFromError(detailErr)
	}
	for _, userToken := range user.Tokens { // Loop through their tokens
		if userToken.Token == token { // If it is the right token
			if userToken.Expiration.Before(time.Now()) { // If token is expired
				webserver.data.Database.UserPurgeExpiredTokens(user.ID.Hex()) // Purge all expired tokens
			} else { // Else token is not expired
				for _, role := range user.Roles { // Loop through roles
					if role == "admin" { // if it is the admin role return
						return user, true, nil
					}
				}
				return user, false, nil // Else user it not admin
			}
			break
		}
	}
	return nil, false, webservermodel.NewErrorMessage("Token not valid.", http.StatusUnauthorized) // If it gets this far the token has not been found
}
