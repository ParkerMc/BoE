package model

import (
	"encoding/json"
)

// Config object for the config file
type Config struct {
	Address  string         `json:"address"`  // Address to be hosted at
	Database ConfigDatabase `json:"database"` // Everything needed for database conection
}

// ConfigDatabase Config subobject for the database in the config
type ConfigDatabase struct {
	Provider string `json:"provider"` // The provider to load
	URL      string `json:"url"`      // The url to the database
	Database string `json:"database"` // The database to use on the server
}

// GetConfigDefault returns the default config
func GetConfigDefault() Config {
	return Config{
		Address: ":8080",
		Database: ConfigDatabase{
			Provider: "mongo",
			URL:      "localhost",
			Database: "boe",
		},
	}
}

// ToJSON converts the object to a json string
func (config *Config) ToJSON() ([]byte, error) {
	return json.MarshalIndent(config, "", " ")
}
