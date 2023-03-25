package config

import (
	"encoding/json"
	"log"
	"os"

	"github.com/disgoorg/snowflake/v2"
)

var OptedOut []snowflake.ID

func init() {
	file, err := os.Open("OptedOut.json")
	if err != nil {
		log.Fatal(err)
	}

	if err = json.NewDecoder(file).Decode(&OptedOut); err != nil {
		log.Fatal(err)
	}
	_ = file.Close()
}
