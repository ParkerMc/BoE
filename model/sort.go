package model

import "strings"

// SortType type for all of the possible formats to sort data in
type SortType string

// All of the sorting types
const (
	SortNone     SortType = "none"
	SortID       SortType = "_id"
	SortName     SortType = "name"
	SortUserName SortType = "username"
)

var sortTypes = map[SortType]string{
	SortID:       "id",
	SortName:     "name",
	SortUserName: "username",
}

// SortTypeFromString returns the sort type from string or none
func SortTypeFromString(sortTypeIn string) SortType {
	for sortType, value := range sortTypes {
		if strings.ToLower(sortTypeIn) == value {
			return sortType
		}
	}
	return SortNone
}
