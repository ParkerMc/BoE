package model

// ErrorType is for all error types to keep from user error
type ErrorType int

// All of the error types
const (
	ErrorBadInput     ErrorType = 0
	ErrorInternal     ErrorType = 1
	ErrorNotFound     ErrorType = 2
	ErrorUnauthorized ErrorType = 3
	ErrorForbidden    ErrorType = 4
	ErrorConflict     ErrorType = 5
)

// Error a detailed version of error so as to provide the right responce code
type Error struct {
	Message string
	Type    ErrorType
}

// NewError create a new error from a string and ErrorType
func NewError(message string, errType ErrorType) *Error {
	return &Error{
		Message: message,
		Type:    errType,
	}
}
