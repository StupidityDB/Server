package main

import (
	"errors"
	"log"
	"net/http"

	"github.com/go-chi/chi"
	"github.com/go-chi/cors"

	"server-go/config"
	"server-go/reviewdb"
	"server-go/stupiditydb"
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

	reviewdb.RegisterRoutes(root)
	stupiditydb.RegisterRoutes(root)

	if err := http.ListenAndServe(":"+config.Config.Port, root); err != nil &&
		!errors.Is(err, http.ErrServerClosed) {
		log.Fatal(err)
	}
}
