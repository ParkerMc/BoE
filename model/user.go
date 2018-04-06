package model

import (
	"strings"
	"time"

	"gopkg.in/mgo.v2/bson"
)

// The hard coded settings for the user
const (
	UserEmailMaxLength    = 255
	UserNameMaxLength     = 60
	UserPasswordMaxLength = 70
	UserPasswordMinLength = 5
	UserUsernameMaxLength = 60
	UserUsernameMinLength = 3
)

// User is the type that stores everything about the user
type User struct {
	ID            bson.ObjectId `bson:"_id,omitempty"`
	Username      string        `bson:"username"`
	Name          string        `bson:"name"`
	Emails        []UserEmail   `bson:"emails"`
	Password      string        `bson:"password"`
	CreatedTs     time.Time     `bson:"created_ts"`
	GlobalRoles   []string      `bson:"global_roles"`
	Tokens        []UserToken   `bson:"tokens"`
	LoginAttempts int           `bson:"login_attempts"`
}

// UserEmail is a subtype of User that stores an email
type UserEmail struct {
	Address  string `json:"address" bson:"address"`
	Verified bool   `json:"verified" bson:"verified"`
}

// UserToken is a subtype of User that store a token
type UserToken struct {
	Token      string    `bson:"token"`
	IP         string    `bson:"ip"`
	Expiration time.Time `bson:"expiration"`
}

// UserCheckEmail checks to make sure the email is within the hard coded settings
func UserCheckEmail(email string) *Error {
	if len(email) > UserEmailMaxLength { // 255 is the longest possible length for an email
		return NewError("Email is too long to be valid.", ErrorBadInput)
	}
	if len(email) == 0 {
		return NewError("email is not provided.", ErrorBadInput)
	}
	// Just a few filters to tell if an email is valid
	if strings.Count(email, "@") > 1 || !strings.Contains(email, "@") || len(strings.Split(email, ".")[strings.Count(email, ".")]) < 2 {
		return NewError("Email is not valid.", ErrorBadInput)
	}
	return nil
}

// UserCheckPassword checks to make sure the email is within the hard coded settings
func UserCheckPassword(password string) *Error {
	if len(password) > UserPasswordMaxLength { // Max length possible password that can be passed through encryption
		return NewError("Password is too long.", ErrorBadInput)
	}
	if len(password) == 0 {
		return NewError("Password is not provided.", ErrorBadInput)
	}
	if len(password) < UserPasswordMinLength { // Min password length to increase security
		return NewError("Password is too short.", ErrorBadInput)
	}
	return nil
}

// UserCheckUsername checks to make sure the email is within the hard coded settings
func UserCheckUsername(username string) *Error {
	if len(username) > UserUsernameMaxLength { // Username max length
		return NewError("Username is too long.", ErrorBadInput)
	}
	if len(username) == 0 {
		return NewError("Username is not provided.", ErrorBadInput)
	}
	if len(username) < UserUsernameMinLength { // Username min length
		return NewError("Username is too short.", ErrorBadInput)
	}
	if strings.Contains(username, "@") { // Make sure the username doesn't contain @
		return NewError("Username must not have \"@\" in it.", ErrorBadInput)
	}
	return nil
}

// UserCheckName checks to make sure the email is within the hard coded settings
func UserCheckName(name string) *Error {
	if len(name) > UserNameMaxLength { // Name max length
		return NewError("Name is too long.", ErrorBadInput)
	}
	if len(name) == 0 {
		return NewError("Name is not provided.", ErrorBadInput)
	}
	return nil
}
