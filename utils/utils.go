package utils

import (
	"math/rand"
	"time"
)

// RandString generates a random string with set length
func RandString(length int) string {
	seededRand := rand.New(rand.NewSource(time.Now().UnixNano())) // Create seeded rand
	b := make([]byte, length)
	for i := range b { // Loop though all elements in array and fill them with a random char
		b[i] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[seededRand.Intn(62)]
	}
	return string(b) // Return it as a string
}
