package model

// Database is the template for all database providers
type Database interface {
	Connect(config *Config, flags *Flags)
	Disconnect()
	UserAddRole(userID string, role string) *Error
	UserCheckPassword(userID string, password string) (bool, *Error)
	UserGetByEmail(email string) (*User, *Error)
	UserGetByID(id string) (*User, *Error)
	UserGetByUsername(username string) (*User, *Error)
	UserGetUsers(page int, pageSize int, sortType SortType) ([]User, *Error)
	UserLogin(userID string, password string, ip string) (*User, *UserToken, *Error)
	UserPurgeExpiredTokens(userID string) *Error
	UserRegister(username string, name string, password string, email string) *Error
	UserRemoveRole(userID string, role string) *Error
	UserSetPassword(userID string, password string) *Error
}
