package webservermodel

import (
	"encoding/json"
	"net/http"

	"github.com/ParkerMc/BoE/model"
	"github.com/ParkerMc/BoE/utils"
)

// UserLoginInput the data passed in when logging in
type UserLoginInput struct {
	UserIdentifier string `json:"user_id"`
	Password       string `json:"password"`
}

// UserLoginResponse the responce set after the user logs in
type UserLoginResponse struct {
	Success bool        `json:"success"`
	Token   string      `json:"token"`
	User    UserPrivate `json:"user"`
}

// UserPrivate the user data that should only be sent to the user or global admins
type UserPrivate struct {
	ID            string            `json:"id"`
	Username      string            `json:"username"`
	Name          string            `json:"name"`
	Emails        []model.UserEmail `json:"emails"`
	CreatedTs     int64             `json:"created_ts"`
	GlobalRoles   []string          `json:"global_roles"`
	LoginAttempts int               `json:"login_attempts"`
}

// UserRegisterInput the data passed in when a user tries to register
type UserRegisterInput struct {
	Username string `json:"username"`
	Name     string `json:"name"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

// ToJSON converts the struct to JSON
func (user *UserLoginResponse) ToJSON() string {
	json, _ := json.Marshal(user)
	return string(json)
}

// Send sends the struct as JSON via http
func (user *UserLoginResponse) Send(w http.ResponseWriter, statusCode int) {
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
		GlobalRoles:   user.GlobalRoles,
		LoginAttempts: user.LoginAttempts,
	}
}

// CheckData checks all the data to make sure it is all valid and has correct length
func (user *UserRegisterInput) CheckData() *model.Error {
	if err := model.UserCheckName(user.Name); err != nil {
		return err
	}
	if err := model.UserCheckEmail(user.Email); err != nil {
		return err
	}
	if err := model.UserCheckPassword(user.Password); err != nil {
		return err
	}
	if err := model.UserCheckUsername(user.Username); err != nil {
		return err
	}
	return nil
}
