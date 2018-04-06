package webservermodel

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/ParkerMc/BoE/model"
)

// Error an more detailed error type
type Error struct {
	Success    bool   `json:"success"`
	Message    string `json:"message"`
	StatusCode int    `json:"-"`
}

// NewError creates a new error from error and a statusCode
func NewError(err error, statusCode int) *Error {
	return &Error{
		Success:    false,
		Message:    err.Error(),
		StatusCode: statusCode,
	}
}

// NewErrorFromError creates a new error from the other more detailed error
func NewErrorFromError(err *model.Error) *Error {
	newError := &Error{
		Success: false,
		Message: err.Message,
	}
	if err.Type == model.ErrorBadInput {
		newError.StatusCode = http.StatusBadRequest
	} else if err.Type == model.ErrorInternal {
		newError.StatusCode = http.StatusInternalServerError
	}
	return newError
}

// NewErrorWithMsg creates new error with message, error, and statusCode
func NewErrorWithMsg(message string, err error, statusCode int) *Error {
	return &Error{
		Success:    false,
		Message:    fmt.Sprintf(message, err.Error()),
		StatusCode: statusCode,
	}
}

// NewErrorMessage creates new error from message and statusCode
func NewErrorMessage(message string, statusCode int) *Error {
	return &Error{
		Success:    false,
		Message:    message,
		StatusCode: statusCode,
	}
}

// Send sends the struct as JSON via http
func (err *Error) Send(w http.ResponseWriter) {
	w.WriteHeader(err.StatusCode)
	w.Write([]byte(err.ToJSON()))
}

// ToJSON converts the struct to JSON
func (err *Error) ToJSON() string {
	json, _ := json.Marshal(err)
	return string(json)
}
