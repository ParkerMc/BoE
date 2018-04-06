package mongo

import (
	"github.com/ParkerMc/BoE/model"
	"github.com/ParkerMc/BoE/utils"
	"gopkg.in/mgo.v2/bson"
)

const settingsCollectionName string = "settings"

// settingsPostConnect Runs after connection to mongo
func (mongo *Mongo) settingsPostConnect() {
	mongo.settings = model.GetSettingsDefault() // Set the default settings
	var settingsResult []model.SettingDB
	err := mongo.database.C(settingsCollectionName).Find(bson.M{}).All(&settingsResult) // Get all the settings from the database
	utils.CheckErrorFatal("Error getting settings from database: %s", err)
	for _, settingName := range model.SettingNames { // Loop though all possible settings
		addSetting := true
		for _, setting := range settingsResult { // Loop though all the settings results
			if setting.GetSettingName() == settingName { // If the setting has the same name then load that setting
				addSetting = false
				mongo.settings[settingName] = setting.ToSetting()
			}
		}
		if addSetting == true { // If the setting is not found in the database add it
			setting := mongo.settings.ToSettingDB(settingName)
			err := mongo.database.C(settingsCollectionName).Insert(setting)
			utils.CheckErrorPrint("Error adding setting to database: %s", err)
		}
	}
}
