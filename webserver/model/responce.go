package webservermodel

import "net/http"

// Responce is for all responses that are not errors
type Responce interface {
	Send(w http.ResponseWriter, statusCode int)
	ToJSON() string
}
