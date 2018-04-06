package mongo

import (
	"fmt"
	"strings"
	"time"

	"github.com/ParkerMc/BoE/model"
	"github.com/ParkerMc/BoE/utils"
	"golang.org/x/crypto/bcrypt"
	"gopkg.in/mgo.v2/bson"
)

const usersCollectionName string = "users"

// UserLogin Attempts to log user in and returns user and token if it can
func (mongo *Mongo) UserLogin(userID string, password string, ip string) (*model.User, *model.UserToken, *model.Error) {
	var query *bson.M
	if strings.Contains(userID, "@") { // If there userID contains a @ then look for and email that matches it
		query = &bson.M{"emails": bson.M{"$elemMatch": bson.M{"address": userID}}}
	} else { // Else look for a username
		query = &bson.M{"username": userID}
	}
	count, err := mongo.database.C(usersCollectionName).Find(query).Count() // Make sure the user exits
	if utils.CheckErrorPrint("Database error while checking if user is valid: %s", err) { // If there is a database error return with it
		return nil, nil, model.NewError(fmt.Sprintf("Database error while checking if user is valid: %s", err), model.ErrorInternal)
	}
	if count == 0 { // If the user count with query is zero then return that the user couldn't be found
		return nil, nil, model.NewError("User not found", model.ErrorBadInput)
	}
	user := &model.User{}
	err = mongo.database.C(usersCollectionName).Find(query).One(user) // Get the user
	if utils.CheckErrorPrint("Database error while getting user: %s", err) { // If there is a database error return with it
		return nil, nil, model.NewError(fmt.Sprintf("Database error while getting user: %s", err), model.ErrorInternal)
	}
	err = bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)) // Check if the password is correct
	if err != nil { // If it is not correct return saying it is incorrect
		// TODO add in user attempts here
		return nil, nil, model.NewError("Password incorrect.", model.ErrorBadInput)
	}
	mongo.UserPurgeExpiredTokens(user.ID.Hex()) // Purges all the expired tokens before creating a new one
	token := model.UserToken{ // Create token
		IP:         ip,
		Expiration: time.Now().Add(time.Duration(mongo.settings.GetInt(model.SettingTokenExpirationDays)*24) * time.Hour),
	}
	for { // Loop keep going until it comes up with a unique token should only take one time
		token.Token = utils.RandString(50) // generate a random string then get a count of all users that have it
		count, err = mongo.database.C(usersCollectionName).Find(bson.M{"tokens": bson.M{"$elemMatch": bson.M{"token": token.Token}}}).Count()
		if utils.CheckErrorPrint("Database error while checking if token is used: %s", err) { // If there is a database error return with it
			return nil, nil, model.NewError(fmt.Sprintf("Database error while checking if token is used: %s", err), model.ErrorInternal)
		}
		if count == 0 { // If there are no users already using the token break the loop
			break
		}
	}
	user.Tokens = append(user.Tokens, token) // Append the token
	err = mongo.database.C(usersCollectionName).Update(bson.M{"_id": user.ID}, bson.M{"$push": bson.M{"tokens": token}}) // Add the token to the user in the database
	if utils.CheckErrorPrint("Database error while adding token to user: %s", err) { // If there is a database error return with it
		return nil, nil, model.NewError(fmt.Sprintf("Database error while adding token to user: %s", err), model.ErrorInternal)
	}
	return user, &token, nil
}

// UserPurgeExpiredTokens Purges all of the expired tokens to keep the tokens clean
func (mongo *Mongo) UserPurgeExpiredTokens(id string) error {
	user := &model.User{} // Get the user from the database
	err := mongo.database.C(usersCollectionName).Find(bson.M{"_id": bson.ObjectIdHex(id)}).One(user)
	if utils.CheckErrorPrint("Database error while getting user: %s", err) { // If there is a database error return with it
		return fmt.Errorf("Database error while getting user: %s", err)
	}
	for _, token := range user.Tokens { // Loop though the tokens
		if token.Expiration.Before(time.Now()) { // If they expired before now tell the database to delete them
			// TODO After cache is added also delete them from there
			err := mongo.database.C(usersCollectionName).Update(bson.M{"_id": user.ID}, bson.M{"$pull": bson.M{"tokens": token}})
			if utils.CheckErrorPrint("Database error while removing token from user: %s", err) { // If there is a database error return with it
				return fmt.Errorf("Database error while removing token from user: %s", err)
			}
		}
	}
	return nil
}

// UserRegister Registers the user
func (mongo *Mongo) UserRegister(username string, name string, password string, email string) *model.Error {
	usersWithUsername, err := mongo.database.C(usersCollectionName).Find(bson.M{"username": username}).Count() // Make sure the username is not already used
	if utils.CheckErrorPrint("Database error while checking if username is used: %s", err) { // If there is a database error return with it
		return model.NewError(fmt.Sprintf("Database error while checking if username is used: %s", err), model.ErrorInternal)
	}
	if usersWithUsername > 0 { // If there is already a user with the username return with error
		return model.NewError("An account with this username already exits", model.ErrorBadInput)
	}
	usersWithEmail, err := mongo.database.C(usersCollectionName).Find(bson.M{"emails": bson.M{"$elemMatch": bson.M{"address": email}}}).Count() // MAke sure that the email is not already used for a user
	if utils.CheckErrorPrint("Database error while checking if email is used: %s", err) { // If there is a database error return with it
		return model.NewError(fmt.Sprintf("Database error while checking if email is used: %s", err), model.ErrorInternal)
	}
	if usersWithEmail > 0 { // If there is already a user with the email return with error
		return model.NewError("An account with this email already exits", model.ErrorBadInput)
	}
	usersRegistered, err := mongo.database.C(usersCollectionName).Find(bson.M{}).Count() // Get a count of how many users are registered
	if utils.CheckErrorPrint("Database error while counting how many users are registered: %s", err) { // If there is a database error return with it
		return model.NewError(fmt.Sprintf("Database error while counting how many users are registered: %s", err), model.ErrorInternal)
	}
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost) // Encrypt the password
	if utils.CheckErrorPrint("Error while creating hash: %s", err) { // If there is an error encrypting return it
		return model.NewError(fmt.Sprintf("Error while creating hash: %s", err), model.ErrorInternal)
	}
	newUser := &model.User{ // Create the new user
		Username: username,
		Name:     name,
		Emails: []model.UserEmail{
			{
				Address:  email,
				Verified: false,
			},
		},
		Password:      string(hash),
		GlobalRoles:   []string{},
		CreatedTs:     time.Now(),
		LoginAttempts: 0,
	}
	if usersRegistered == 0 { // If this is the first user give it admin
		newUser.GlobalRoles = []string{"admin"}
	}
	err = mongo.database.C(usersCollectionName).Insert(newUser) // Insert the user into database
	if utils.CheckErrorPrint("Database error while creating user: %s", err) { // If there is a database error return with it
		return model.NewError(fmt.Sprintf("Database error while creating user: %s", err), model.ErrorInternal)
	}
	return nil
}
