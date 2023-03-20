package config

import (
	"encoding/json"
	"log"
	"os"
)

var OptedOut = []uint64{}

func init() {
	file, err := os.Open("optedOut.json")
	if err != nil {
		log.Fatal(err)
	}

	if err = json.NewDecoder(file).Decode(&OptedOut); err != nil {
		log.Fatal(err)
	}

	_ = file.Close()
}
