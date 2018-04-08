package webservermodel

import (
	"encoding/json"
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

// CheckData checks all the data to make sure it is all valid and has correct length
func (user *UserRegisterInput) CheckData() *Error {
	if err := model.UserCheckName(user.Name); err != nil {
		return NewErrorFromError(err)
	}
	if err := model.UserCheckEmail(user.Email); err != nil {
		return NewErrorFromError(err)
	}
	if err := model.UserCheckPassword(user.Password); err != nil {
		return NewErrorFromError(err)
	}
	if err := model.UserCheckUsername(user.Username); err != nil {
		return NewErrorFromError(err)
	}
	return nil
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
