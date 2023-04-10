package main

import (
	"errors"
	"log"
	"net/http"

	"github.com/go-chi/chi"
	"github.com/go-chi/cors"

	"server-go/config"
)

func main() {
	root := chi.NewRouter()
	root.Use(
		cors.Handler(
			cors.Options{
				AllowedOrigins: []string{"*"},
				AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
				AllowedHeaders: []string{"*"},
			},
		),
	)

	if err := http.ListenAndServe(":"+config.Config.Port, root); err != nil &&
		!errors.Is(err, http.ErrServerClosed) {
		log.Fatal(err)
	}
}
