package config

import (
	"encoding/json"
	"log"
	"os"
)

type dbConfig struct {
	IP       string `json:"ip"`
	User     string `json:"user"`
	Name     string `json:"name"`
	Password string `json:"password"`
}

type clientConfig struct {
	ID     string `json:"id"`
	Secret string `json:"secret"`
}

type config struct {
	DBConfig     *dbConfig     `json:"db"`
	ClientConfig *clientConfig `json:"client"`
}

var Config *config

func init() {
	file, err := os.Open("config.json")
	if err != nil {
		log.Fatal(err)
	}

	if err = json.NewDecoder(file).Decode(&Config); err != nil {
		log.Fatal(err)
	}

	_ = file.Close()
}
