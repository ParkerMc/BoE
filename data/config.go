package data

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/ParkerMc/BoE/model"
	"github.com/ParkerMc/BoE/utils"
)

// initConfig Init's the config module
func (data *Data) initConfig() {
	data.Config = model.GetConfigDefault()
}

// LoadConfig Loads the config
func (data *Data) LoadConfig() {
	if _, err := os.Stat(data.Flags.ConfigFile); err == nil { // If the file exists
		configFile, err := os.Open(data.Flags.ConfigFile) // Read it
		utils.CheckErrorFatal("Error while loading config: %s", err)
		jsonParser := json.NewDecoder(configFile) // Decode the json
		jsonParser.Decode(&data.Config)
		configFile.Close()
	}
	if _, err := os.Stat(filepath.Dir(data.Flags.ConfigFile)); os.IsNotExist(err) { // If the folder doesn't exist create it
		err = os.MkdirAll(filepath.Dir(data.Flags.ConfigFile), 0655)
		utils.CheckErrorPrint("Error while creating folder for config config: %s", err)
	}
	configJSON, err := data.Config.ToJSON() // Get a string from the config
	utils.CheckErrorPrint("Error while converting the config object to json: %s", err)
	err = ioutil.WriteFile(data.Flags.ConfigFile, configJSON, 0655) // Write it to the file
	utils.CheckErrorPrint("Error while saving config: %s", err)
}
