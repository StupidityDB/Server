package config

import (
	"encoding/json"
	"log"
	"os"

	goaway "github.com/TwiN/go-away"
)

var ProfanityDetector *goaway.ProfanityDetector

func init() {
	file, err := os.Open("ProfaneWordList.json")
	if err != nil {
		log.Fatal(err)
	}

	var profaneWords []string

	if err = json.NewDecoder(file).Decode(&profaneWords); err != nil {
		log.Fatal(err)
	}

	ProfanityDetector = goaway.NewProfanityDetector().WithCustomDictionary(profaneWords, nil, nil)
}
