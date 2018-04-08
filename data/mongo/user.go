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

// UserAddRole Adds a role to the user
func (mongo *Mongo) UserAddRole(userID string, role string) *model.Error {
	user, detailErr := mongo.UserFromID(userID)
	if detailErr != nil { // If there is an error return it
		return detailErr
	}
	for _, userRole := range user.Roles { // Loop through the roles
		if userRole == role { // If it is the role error and say that they already have the role
			return model.NewError("User already has this role", model.ErrorBadInput)
		}
	}
	user.Roles = append(user.Roles, role) // Add the role to the user in the cache

	err := mongo.database.C(usersCollectionName).Update(bson.M{"_id": user.ID}, bson.M{"$push": bson.M{"roles": role}}) // Add the role to the user in the database
	if utils.CheckErrorPrint("Database error while adding role to user: %s", err) {                                     // If there is a database error return with it
		return model.NewError(fmt.Sprintf("Database error while adding role to user: %s", err), model.ErrorInternal)
	}
	return nil
}

// UserCheckPassword Checks to see if password is correct DO NOT use for authing
func (mongo *Mongo) UserCheckPassword(userID string, password string) (bool, *model.Error) {
	user, detailErr := mongo.UserFromID(userID)
	if detailErr != nil { // If there is an error return it
		return false, detailErr
	}
	err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)) // Check if the password is correct
	if err != nil {                                                               // If it is not correct return saying it is incorrect
		return false, nil
	}
	return true, nil
}

func (mongo *Mongo) userClearCache() {
	mongo.userCache = mongo.userCache[:0]
}

// UserFromEmail returns user with given email
func (mongo *Mongo) UserFromEmail(email string) (*model.User, *model.Error) {
	for i := range mongo.userCache { // Loop through the cache
		for _, userEmail := range mongo.userCache[i].Emails { // Loop through the emails for the user
			if userEmail.Address == email { // If the email matches an entry return it
				return &mongo.userCache[i], nil
			}
		}
	}
	user, detailErr := mongo.userGet(bson.M{"emails": bson.M{"$elemMatch": bson.M{"address": email}}}) // Get the user
	if detailErr != nil {                                                                              // If there is an error return it
		return nil, detailErr
	}
	return user, nil
}

// UserFromID returns user with given id
func (mongo *Mongo) UserFromID(id string) (*model.User, *model.Error) {
	if !bson.IsObjectIdHex(id) { // Make sure the id is a valid id
		return nil, model.NewError("Not valid ID", model.ErrorBadInput)
	}
	for i := range mongo.userCache { // Loop through the cache
		if mongo.userCache[i].ID.Hex() == id { // If the ids matches an entry return it
			return &mongo.userCache[i], nil
		}
	}
	user, detailErr := mongo.userGet(bson.M{"_id": bson.ObjectIdHex(id)}) // Get the user
	if detailErr != nil {                                                 // If there is an error return it
		return nil, detailErr
	}
	return user, nil
}

// UserFromUsername returns user with given username
func (mongo *Mongo) UserFromUsername(username string) (*model.User, *model.Error) {
	for i := range mongo.userCache { // Loop through the cache
		if mongo.userCache[i].Username == username { // If the usernames matches an entry return it
			return &mongo.userCache[i], nil
		}
	}
	user, detailErr := mongo.userGet(bson.M{"username": username}) // Get the user
	if detailErr != nil {                                          // If there is an error return it
		return nil, detailErr
	}
	return user, nil
}

func (mongo *Mongo) userGet(query bson.M) (*model.User, *model.Error) {
	count, err := mongo.database.C(usersCollectionName).Find(query).Count()               // Make sure the user exits
	if utils.CheckErrorPrint("Database error while checking if user is valid: %s", err) { // If there is a database error return with it
		return nil, model.NewError(fmt.Sprintf("Database error while checking if user is valid: %s", err), model.ErrorInternal)
	}
	if count == 0 { // If the user count with query is zero then return that the user couldn't be found
		return nil, model.NewError("User not found", model.ErrorNotFound)
	}
	user := model.User{}
	err = mongo.database.C(usersCollectionName).Find(query).One(&user)       // Get the user
	if utils.CheckErrorPrint("Database error while getting user: %s", err) { // If there is a database error return with it
		return nil, model.NewError(fmt.Sprintf("Database error while getting user: %s", err), model.ErrorInternal)
	}
	if len(mongo.userCache) >= mongo.settings.GetInt(model.SettingUserCacheSize) { // if the user cache is bigger or at the cache size then drop the first item
		mongo.userCache = append(mongo.userCache[:0], mongo.userCache[1:]...)
	}
	mongo.userCache = append(mongo.userCache, user) // append the user to the cache

	return &user, nil
}

// UserGetUsers gets users from prams
func (mongo *Mongo) UserGetUsers(page int, pageSize int, sortType model.SortType) ([]model.User, *model.Error) {
	query := bson.M{}                                                          // Add changes to query for later
	count, err := mongo.database.C(usersCollectionName).Find(query).Count()    // Get the number of users that match the query
	if utils.CheckErrorPrint("Database error while counting users: %s", err) { // If there is a database error return with it
		return nil, model.NewError(fmt.Sprintf("Database error while counting users: %s", err), model.ErrorInternal)
	}
	if page*pageSize >= count { // If the page is out of range return error
		return nil, model.NewError("Page given out of range", model.ErrorBadInput)
	}
	var users []model.User // Get the users that match the query then the page
	mongo.database.C(usersCollectionName).Find(query).Sort(string(sortType)).Skip(page * pageSize).Limit(pageSize).All(&users)
	if utils.CheckErrorPrint("Database error while getting users: %s", err) { // If there is a database error return with it
		return nil, model.NewError(fmt.Sprintf("Database error while getting users: %s", err), model.ErrorInternal)
	}
	return users, nil
}

func (mongo *Mongo) userInit() {
	mongo.userCache = make([]model.User, 0) // create the cache array
}

// UserLogin Attempts to log user in and returns user and token if it can
func (mongo *Mongo) UserLogin(userID string, password string, ip string) (*model.User, *model.UserToken, *model.Error) {
	var user *model.User
	var detailErr *model.Error
	if strings.Contains(userID, "@") { // If there userID contains a @ then get user by email
		user, detailErr = mongo.UserFromEmail(userID)
	} else { // Else look for a user by username
		user, detailErr = mongo.UserFromUsername(userID)
	}
	if detailErr != nil { // If there is an error return it
		return nil, nil, detailErr
	}
	err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)) // Check if the password is correct
	if err != nil {                                                               // If it is not correct return saying it is incorrect
		// TODO add in user attempts here
		return nil, nil, model.NewError("Password incorrect.", model.ErrorUnauthorized)
	}
	mongo.UserPurgeExpiredTokens(user.ID.Hex()) // Purges all the expired tokens before creating a new one
	token := model.UserToken{                   // Create token
		IP:         ip,
		Expiration: time.Now().Add(time.Duration(mongo.settings.GetInt(model.SettingTokenExpirationDays)*24) * time.Hour),
	}
	for { // Loop keep going until it comes up with a unique token should only take one time
		token.Token = utils.RandString(50) // generate a random string then get a count of all users that have it
		count, dbErr := mongo.database.C(usersCollectionName).Find(bson.M{"tokens": bson.M{"$elemMatch": bson.M{"token": token.Token}}}).Count()
		if utils.CheckErrorPrint("Database error while checking if token is used: %s", dbErr) { // If there is a database error return with it
			return nil, nil, model.NewError(fmt.Sprintf("Database error while checking if token is used: %s", dbErr), model.ErrorInternal)
		}
		if count == 0 { // If there are no users already using the token break the loop
			break
		}
	}
	user.Tokens = append(user.Tokens, token)                                                                             // Append the token
	err = mongo.database.C(usersCollectionName).Update(bson.M{"_id": user.ID}, bson.M{"$push": bson.M{"tokens": token}}) // Add the token to the user in the database
	if utils.CheckErrorPrint("Database error while adding token to user: %s", err) {                                     // If there is a database error return with it
		return nil, nil, model.NewError(fmt.Sprintf("Database error while adding token to user: %s", err), model.ErrorInternal)
	}
	return user, &token, nil
}

// UserPurgeExpiredTokens Puges all of the expired tokens
func (mongo *Mongo) UserPurgeExpiredTokens(userID string) *model.Error {
	user, detailErr := mongo.UserFromID(userID)
	if detailErr != nil {
		return detailErr
	}
	toRemove := make([]model.UserToken, 0) // List of tokens to remove
	for _, token := range user.Tokens {    // Loop though the tokens
		if token.Expiration.Before(time.Now()) { // If they expired before now tell the database to delete them
			toRemove = append(toRemove, token)
			err := mongo.database.C(usersCollectionName).Update(bson.M{"_id": bson.ObjectIdHex(userID)}, bson.M{"$pull": bson.M{"tokens": token}})
			if utils.CheckErrorPrint("Database error while removing token from user: %s", err) { // If there is a database error return with it
				return model.NewError(fmt.Sprintf("Database error while removing token from user: %s", err), model.ErrorInternal)
			}
		}
	}
	for _, token := range toRemove { // Loop through the list of tokens to remove
		for i, userToken := range user.Tokens {
			if token == userToken {
				user.Tokens = append(user.Tokens[:i], user.Tokens[i+1:]...)
				break
			}
		}
	}
	return nil
}

// UserRegister Registers the user
func (mongo *Mongo) UserRegister(username string, name string, password string, email string) *model.Error {
	_, detailErr := mongo.UserFromUsername(username)
	if detailErr != nil && detailErr.Type != model.ErrorNotFound { // If there is a database error return with it
		return detailErr
	}
	if detailErr == nil { // If there is no error then user was found return saying username was taken
		return model.NewError("Username taken.", model.ErrorBadInput)
	}
	_, detailErr = mongo.UserFromEmail(email)
	if detailErr != nil && detailErr.Type != model.ErrorNotFound { // If there is a database error return with it
		return detailErr
	}
	if detailErr == nil { // If there is no error then user was found return saying email was taken
		return model.NewError("Email taken.", model.ErrorBadInput)
	}
	usersRegistered, err := mongo.database.C(usersCollectionName).Find(bson.M{}).Count()               // Get a count of how many users are registered
	if utils.CheckErrorPrint("Database error while counting how many users are registered: %s", err) { // If there is a database error return with it
		return model.NewError(fmt.Sprintf("Database error while counting how many users are registered: %s", err), model.ErrorInternal)
	}
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost) // Encrypt the password
	if utils.CheckErrorPrint("Error while creating hash: %s", err) {               // If there is an error encrypting return it
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
		Roles:         []string{},
		CreatedTs:     time.Now(),
		LoginAttempts: 0,
	}
	if usersRegistered == 0 { // If this is the first user give it admin
		newUser.Roles = []string{"admin"}
	}
	err = mongo.database.C(usersCollectionName).Insert(newUser)               // Insert the user into database
	if utils.CheckErrorPrint("Database error while creating user: %s", err) { // If there is a database error return with it
		return model.NewError(fmt.Sprintf("Database error while creating user: %s", err), model.ErrorInternal)
	}
	return nil
}

// UserRemoveRole Removes a role from a user
func (mongo *Mongo) UserRemoveRole(userID string, role string) *model.Error {
	user, detailErr := mongo.UserFromID(userID)
	if detailErr != nil { // If there is an error return it
		return detailErr
	}
	for i, userRole := range user.Roles { // Loop through the roles array if it is the right role remove it
		if userRole == role {
			user.Roles = append(user.Roles[:i], user.Roles[i+1:]...)                                                            // Remove the role from the user in the cache
			err := mongo.database.C(usersCollectionName).Update(bson.M{"_id": user.ID}, bson.M{"$pull": bson.M{"roles": role}}) // Remove the role from the user in the database
			if utils.CheckErrorPrint("Database error while removing role from user: %s", err) {                                 // If there is a database error return with it
				return model.NewError(fmt.Sprintf("Database error while removing role from user: %s", err), model.ErrorInternal)
			}
			return nil
		}
	}

	return model.NewError("User doesn't has this role", model.ErrorBadInput) // Else the user doesn't have the role so return with error
}

// UserSetPassword sets the password for the user
func (mongo *Mongo) UserSetPassword(userID string, password string) *model.Error {
	user, detailErr := mongo.UserFromID(userID)
	if detailErr != nil { // If there is an error return it
		return detailErr
	}
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost) // Encrypt the password
	if utils.CheckErrorPrint("Error while creating hash: %s", err) {               // If there is an error encrypting return it
		return model.NewError(fmt.Sprintf("Error while creating hash: %s", err), model.ErrorInternal)
	}
	user.Password = string(hash)                                                                                                 // Set the user password in the cache
	err = mongo.database.C(usersCollectionName).Update(bson.M{"_id": user.ID}, bson.M{"$set": bson.M{"password": string(hash)}}) // Set the password in the database
	if utils.CheckErrorPrint("Error updating password in database: %s", err) {                                                   // If there is an error encrypting return it
		return model.NewError(fmt.Sprintf("Error updating password in database: %s", err), model.ErrorInternal)
	}
	return nil
}
