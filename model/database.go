package model

// Database is the template for all database providers
type Database interface {
	Connect(config *Config, flags *Flags)
	Disconnect()
	UserLogin(userID string, password string, ip string) (*User, *UserToken, *Error)
	UserPurgeExpiredTokens(id string) error
	UserRegister(username string, name string, password string, email string) *Error
}
