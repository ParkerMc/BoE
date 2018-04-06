package data

import (
	"flag"
	"os"
	"runtime"
)

// ParseFlags Parses the flags given from command */
func (data *Data) ParseFlags() {
	flag.BoolVar(&data.Flags.Debug, "debug", false, "Enables debuging") // Enables debuging
	defaultConfig := "config.json"                                      // The default config file
	if runtime.GOOS == "linux" && os.Getenv("ENV") != "DEV" {           // If the os is linux and the ENV varable isn't DEV then change the default config
		defaultConfig = "/etc/boe/config.json"
	}
	flag.StringVar(&data.Flags.ConfigFile, "config", defaultConfig, "Set the config file") // Sets the config file to use
	flag.Parse()
}
