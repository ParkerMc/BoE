package main

import (
	"log"
	"os"
	"os/signal"

	"github.com/ParkerMc/BoE/data"
	"github.com/ParkerMc/BoE/webserver"
)

func main() {
	dataStore := data.Init()
	dataStore.ParseFlags()
	dataStore.LoadConfig()
	dataStore.ConnectToDatabase()
	webServer := webserver.Init(dataStore)
	webServer.Start()

	stopSignal := make(chan os.Signal, 1)
	signal.Notify(stopSignal, os.Interrupt)
	for range stopSignal {
		log.Print("Got interrupt signal. Stoping")
		dataStore.Database.Disconnect()
		webServer.Stop()
		os.Exit(0)
	}
}
