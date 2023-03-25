package config

import (
	"encoding/json"
	"log"
	"os"
)

type dbConfig struct {
	IP       string `json:"IP"`
	User     string `json:"User"`
	Name     string `json:"Name"`
	Password string `json:"Password"`
}

type config struct {
	DB   *dbConfig `json:"DB"`
	Port string    `json:"Port"`
}

var Config *config

func init() {
	file, err := os.Open("Config.json")
	if err != nil {
		log.Fatal(err)
	}

	if err = json.NewDecoder(file).Decode(&Config); err != nil {
		log.Fatal(err)
	}

	_ = file.Close()
}
