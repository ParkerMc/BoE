package webservermodel

import (
	"encoding/json"
	"io"
	"net/http"

	"github.com/ParkerMc/BoE/model"
	"github.com/ParkerMc/BoE/utils"
)

// UserChangePasswordInput the data passed in when changeing password
type UserChangePasswordInput struct {
	CurrentPassword string `json:"current_password"`
	NewPassword     string `json:"new_password"`
}

// UserLoginInput the data passed in when logging in
type UserLoginInput struct {
	UserIdentifier string `json:"user_id"`
	Password       string `json:"password"`
}

// UserLoginResponse the responce set after the user logs in
type UserLoginResponse struct {
	Token string      `json:"token"`
	User  UserPrivate `json:"user"`
}

// UserPrivateResponse the responce that returns a single private user to themself or an admin
type UserPrivateResponse struct {
	User UserPrivate `json:"user"`
}

// UserPublicResponse the responce that returns a single public user
type UserPublicResponse struct {
	User UserPublic `json:"user"`
}

// UserPrivate the user data that should only be sent to the user or global admins
type UserPrivate struct {
	ID            string            `json:"id"`
	Username      string            `json:"username"`
	Name          string            `json:"name"`
	Emails        []model.UserEmail `json:"emails"`
	CreatedTs     int64             `json:"created_ts"`
	Roles         []string          `json:"roles"`
	LoginAttempts int               `json:"login_attempts"`
}

// UserPublic the user data that can be sent to anyone loged in
type UserPublic struct {
	ID            string   `json:"id"`
	Username      string   `json:"username"`
	Name          string   `json:"name"`
	CreatedTs     int64    `json:"created_ts"`
	Roles         []string `json:"roles"`
	LoginAttempts int      `json:"login_attempts"`
}

// UserRegisterInput the data passed in when a user tries to register
type UserRegisterInput struct {
	Username string `json:"username"`
	Name     string `json:"name"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

// UsersPrivateResponse the responce that returns many private users to an admin
type UsersPrivateResponse struct {
	Users []UserPrivate `json:"users"`
}

// UsersPublicResponse the responce that returns many public users
type UsersPublicResponse struct {
	Users []UserPublic `json:"users"`
}

// UserChangePasswordInputFromJSON Gets UserChangePasswordInput object from json
func UserChangePasswordInputFromJSON(body io.ReadCloser) (*UserChangePasswordInput, *Error) {
	changePasswordIn := &UserChangePasswordInput{} // Get the password change object from the body
	err := json.NewDecoder(body).Decode(changePasswordIn)
	if err != nil { // If there and an erorr sned it
		return nil, NewErrorWithMsg("Error decoding json: %s", err, http.StatusBadRequest)
	}
	if changePasswordIn.NewPassword == "" { // If there is no new password send error
		return nil, NewErrorMessage("new_password must not be blank", http.StatusBadRequest)
	}
	return changePasswordIn, nil
}

// UserLoginInputFromJSON Gets UserRegisterInput object from json and checks the data
func UserLoginInputFromJSON(body io.ReadCloser) (*UserLoginInput, *Error) {
	user := &UserLoginInput{}
	err := json.NewDecoder(body).Decode(user) // Decode the body
	if err != nil {                           // If there is an error return it
		return nil, NewErrorWithMsg("Error decoding json: %s", err, http.StatusBadRequest)
	}
	if user.UserIdentifier == "" {
		return nil, NewErrorMessage("user_id must not be empty.", http.StatusBadRequest)

	}
	if user.Password == "" {
		return nil, NewErrorMessage("password must not be empty.", http.StatusBadRequest)

	}
	return user, nil
}

// ToJSON converts the struct to JSON
func (user UserLoginResponse) ToJSON() string {
	json, _ := json.Marshal(user)
	return string(json)
}

// Send sends the struct as JSON via http
func (user UserLoginResponse) Send(w http.ResponseWriter, statusCode int) {
	w.WriteHeader(statusCode)
	w.Write([]byte(user.ToJSON()))
}

// ToJSON converts the struct to JSON
func (user UserPrivateResponse) ToJSON() string {
	json, _ := json.Marshal(user)
	return string(json)
}

// Send sends the struct as JSON via http
func (user UserPrivateResponse) Send(w http.ResponseWriter, statusCode int) {
	w.WriteHeader(statusCode)
	w.Write([]byte(user.ToJSON()))
}

// ToJSON converts the struct to JSON
func (user UserPublicResponse) ToJSON() string {
	json, _ := json.Marshal(user)
	return string(json)
}

// Send sends the struct as JSON via http
func (user UserPublicResponse) Send(w http.ResponseWriter, statusCode int) {
	w.WriteHeader(statusCode)
	w.Write([]byte(user.ToJSON()))
}

// UserPrivateFromUser returns UserPrivate from model.User
func UserPrivateFromUser(user *model.User) UserPrivate {
	return UserPrivate{
		ID:            user.ID.Hex(),
		Username:      user.Username,
		Name:          user.Name,
		Emails:        user.Emails,
		CreatedTs:     utils.MillisFromTime(user.CreatedTs),
		Roles:         user.Roles,
		LoginAttempts: user.LoginAttempts,
	}
}

// UserPublicFromUser returns UserPublic from model.User
func UserPublicFromUser(user *model.User) UserPublic {
	return UserPublic{
		ID:            user.ID.Hex(),
		Username:      user.Username,
		Name:          user.Name,
		CreatedTs:     utils.MillisFromTime(user.CreatedTs),
		Roles:         user.Roles,
		LoginAttempts: user.LoginAttempts,
	}
}

// UserRegisterInputFromJSON Gets UserRegisterInput object from json and checks the data
func UserRegisterInputFromJSON(body io.ReadCloser) (*UserRegisterInput, *Error) {
	user := &UserRegisterInput{}
	err := json.NewDecoder(body).Decode(user) // Decode the body
	if err != nil {                           // If there is an error return it
		return nil, NewErrorWithMsg("Error decoding json: %s", err, http.StatusBadRequest)
	}
	if err := model.UserCheckName(user.Name); err != nil { // Check the name if there is an error return it
		return nil, NewErrorFromError(err)
	}
	if err := model.UserCheckEmail(user.Email); err != nil { // Check the email if there is an error return it
		return nil, NewErrorFromError(err)
	}
	if err := model.UserCheckPassword(user.Password); err != nil { // Check the password if there is an error return it
		return nil, NewErrorFromError(err)
	}
	if err := model.UserCheckUsername(user.Username); err != nil { // Check the username if there is an error return it
		return nil, NewErrorFromError(err)
	}
	return user, nil
}

// ToJSON converts the struct to JSON
func (user UsersPrivateResponse) ToJSON() string {
	json, _ := json.Marshal(user)
	return string(json)
}

// Send sends the struct as JSON via http
func (user UsersPrivateResponse) Send(w http.ResponseWriter, statusCode int) {
	w.WriteHeader(statusCode)
	w.Write([]byte(user.ToJSON()))
}

// ToJSON converts the struct to JSON
func (user UsersPublicResponse) ToJSON() string {
	json, _ := json.Marshal(user)
	return string(json)
}

// Send sends the struct as JSON via http
func (user UsersPublicResponse) Send(w http.ResponseWriter, statusCode int) {
	w.WriteHeader(statusCode)
	w.Write([]byte(user.ToJSON()))
}
