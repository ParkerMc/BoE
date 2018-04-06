package utils

import "time"

// MillisFromTime converts time to milliseconds
func MillisFromTime(t time.Time) int64 {
	return t.UnixNano() / int64(time.Millisecond)
}
