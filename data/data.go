package data

import (
	"log"

	"github.com/ParkerMc/BoE/data/mongo"
	"github.com/ParkerMc/BoE/model"
)

// Data Handles all data that is stored
type Data struct {
	Config   model.Config
	Flags    model.Flags
	Database model.Database
}

// Init Inits the data type
func Init() *Data {
	data := &Data{}

	// Run init for everything
	data.initConfig()

	return data
}

// ConnectToDatabase Connects to the database
func (data *Data) ConnectToDatabase() {
	if data.Config.Database.Provider == "mongo" {
		data.Database = mongo.Init()
		data.Database.Connect(&data.Config, &data.Flags)
	} else {
		log.Fatalf("Unknown database provider: %s", data.Config.Database.Provider)
	}
}
