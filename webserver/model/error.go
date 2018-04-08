package webservermodel

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/ParkerMc/BoE/model"
)

// Error an more detailed error type
type Error struct {
	Message    string `json:"message"`
	StatusCode int    `json:"-"`
}

// NewError creates a new error from error and a statusCode
func NewError(err error, statusCode int) *Error {
	return &Error{
		Message:    err.Error(),
		StatusCode: statusCode,
	}
}

// NewErrorFromError creates a new error from the other more detailed error
func NewErrorFromError(detailErr *model.Error) *Error {
	newError := &Error{
		Message: detailErr.Message,
	}
	if detailErr.Type == model.ErrorBadInput {
		newError.StatusCode = http.StatusBadRequest
	} else if detailErr.Type == model.ErrorInternal {
		newError.StatusCode = http.StatusInternalServerError
	} else if detailErr.Type == model.ErrorNotFound {
		newError.StatusCode = http.StatusNotFound
	} else if detailErr.Type == model.ErrorUnauthorized {
		newError.StatusCode = http.StatusUnauthorized
	} else if detailErr.Type == model.ErrorForbidden {
		newError.StatusCode = http.StatusForbidden
	}
	return newError
}

// NewErrorWithMsg creates new error with message, error, and statusCode
func NewErrorWithMsg(message string, err error, statusCode int) *Error {
	return &Error{
		Message:    fmt.Sprintf(message, err.Error()),
		StatusCode: statusCode,
	}
}

// NewErrorMessage creates new error from message and statusCode
func NewErrorMessage(message string, statusCode int) *Error {
	return &Error{
		Message:    message,
		StatusCode: statusCode,
	}
}

// Send sends the struct as JSON via http
func (webErr *Error) Send(w http.ResponseWriter) {
	w.WriteHeader(webErr.StatusCode)
	w.Write([]byte(webErr.ToJSON()))
}

// ToJSON converts the struct to JSON
func (webErr *Error) ToJSON() string {
	json, _ := json.Marshal(webErr)
	return string(json)
}
