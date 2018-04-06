package utils

import "log"

// CheckErrorPrint if there is an error then print it
func CheckErrorPrint(errorText string, err error) bool {
	if err != nil {
		log.Printf(errorText, err.Error())
		return true
	}
	return false
}

// CheckErrorFatal if there is an error then print it as fatal
func CheckErrorFatal(errorText string, err error) bool {
	if err != nil {
		log.Fatalf(errorText, err.Error())
		return true
	}
	return false
}
