package model

import (
	"strconv"

	"github.com/ParkerMc/BoE/utils"
)

// SettingName is a type to store all setting's name to prevent human error
type SettingName string

// All of the setting names
const (
	SettingUserCacheSize       SettingName = "user_cache_size"
	SettingServerCacheSize     SettingName = "server_cache_size"
	SettingChannelCacheSize    SettingName = "channel_cache_size"
	SettingMessageCacheSize    SettingName = "message_cache_size"
	SettingTokenExpirationDays SettingName = "token_expiration_days"
)

// SettingNames is an array of all settings to keep from having to edit the database code individual;y
var SettingNames = []SettingName{
	SettingUserCacheSize,
	SettingServerCacheSize,
	SettingChannelCacheSize,
	SettingMessageCacheSize,
	SettingTokenExpirationDays,
}

// Settings is used as the type to store all the settings in
type Settings map[SettingName]Setting

// SettingDB is how to a setting is stored in the database
type SettingDB struct {
	Name  string `bson:"name"`
	Type  string `bson:"type"`
	Value string `bson:"value"`
}

// Setting is for the setting in its array
type Setting struct {
	Type  string
	Value string
}

// GetSettingsDefault returns all the default settings
func GetSettingsDefault() Settings {
	return Settings{
		SettingUserCacheSize:       {Type: "int", Value: "50"},
		SettingServerCacheSize:     {Type: "int", Value: "10"},
		SettingChannelCacheSize:    {Type: "int", Value: "50"},
		SettingMessageCacheSize:    {Type: "int", Value: "2000"},
		SettingTokenExpirationDays: {Type: "int", Value: "15"},
	}
}

// String returns the setting name as string
func (settingName SettingName) String() string {
	return string(settingName)
}

// GetSettingName Gets the setting name
func (setting *SettingDB) GetSettingName() SettingName {
	for _, settingName := range SettingNames { // Loop though the array of names
		if string(settingName) == setting.Name { // If it is the same name as the setting type then return it
			return settingName
		}
	}
	return "" // Else return blank
}

// Get gets the setting as string
func (settings Settings) Get(name SettingName) string {
	return settings[name].Value
}

// GetInt returns the setting as int
func (settings Settings) GetInt(name SettingName) int {
	if settings[name].Type == "int" { // If type is int return it as int
		out, err := strconv.Atoi(settings[name].Value)
		utils.CheckErrorPrint("Error converting setting to int: %s", err)
		return out
	}
	return 0 // Else return 0
}

// GetType returns the type that the setting is
func (settings Settings) GetType(name SettingName) string {
	return settings[name].Type
}

// ToSetting converts the setting database type to setting
func (setting *SettingDB) ToSetting() Setting {
	return Setting{
		Type:  setting.Type,
		Value: setting.Value,
	}
}

// ToSettingDB converts the setting to the setting database type
func (settings Settings) ToSettingDB(name SettingName) SettingDB {
	return SettingDB{
		Name:  string(name),
		Type:  settings[name].Type,
		Value: settings[name].Value,
	}
}
