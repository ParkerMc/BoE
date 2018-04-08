package mongo

import (
	"log"
	"time"

	"github.com/ParkerMc/BoE/model"
	mgo "gopkg.in/mgo.v2"
)

// Mongo is the database provider
type Mongo struct {
	config   *model.Config
	flags    *model.Flags
	session  *mgo.Session
	database *mgo.Database

	settings  model.Settings
	userCache []model.User
}

// Init Inits for the mongo database
func Init() *Mongo {
	mongo := Mongo{}

	mongo.userInit()

	return &mongo
}

// Connect connects to the databse
func (mongo *Mongo) Connect(config *model.Config, flags *model.Flags) {
	mongo.config = config
	mongo.flags = flags

	for try := 0; try < 5; try++ { // Try to connect to the database 5 times before giving up
		log.Print("Attempting to connect to the database.")
		var err error
		mongo.session, err = mgo.Dial(mongo.config.Database.URL) // Dial up the databse
		if err == nil {                                          // If there is no error then the connection was made
			log.Print("Connected to the database.")
			break // Exit the loop
		}
		log.Printf("Error connecting to the database: %s", err.Error())
		if try > 3 { // If was the last try send a fatal error
			log.Fatal("Failed to connect to the database after five attempts.")
		}
		log.Print("Attempting database connection again in five seconds.")
		time.Sleep(5 * time.Second) // Sleep for five seconds before trying to connect again
	}
	mongo.session.SetMode(mgo.Monotonic, true)                        // Turn monotonic mode on
	mongo.database = mongo.session.DB(mongo.config.Database.Database) // Set the database to the right one
	mongo.postConnect()
}

// postConnect Runs right after database connection
func (mongo *Mongo) postConnect() {
	mongo.settingsPostConnect()
}

// Disconnect Disconnects from the database
func (mongo *Mongo) Disconnect() {
	mongo.session.Clone()
}
