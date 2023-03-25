package main

import (
	"errors"
	"log"
	"net/http"

	"github.com/go-chi/chi"

	"server-go/config"
)

type StupidityDBServer struct {
	*chi.Mux
}

func (s *StupidityDBServer) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// CORS
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")

	s.Mux.ServeHTTP(w, r)
}

func main() {
	root := &StupidityDBServer{chi.NewRouter()}

	api := chi.NewRouter()
	root.Mount("/api", api)

	apiUsers := chi.NewRouter()
	api.Mount("/users", apiUsers)

	if err := http.ListenAndServe(":"+config.Config.Port, root); err != nil && !errors.Is(err, http.ErrServerClosed) {
		log.Fatal(err)
	}
}
