package stupiditydb

import (
	"net/http"
	"strconv"

	"github.com/go-chi/chi"
)

func RegisterRoutes(r chi.Router) {
	r.Get("/api/users/{UserID}/stupidity", GetStupidity)
	r.Put("/api/users/{UserID}/stupidity", PutStupidity)
}

func GetStupidity(w http.ResponseWriter, r *http.Request) {
	userID, err := strconv.Atoi(chi.URLParam(r, "UserID"))
	if err != nil {
		// TODO: Handle error
		return
	}

	stupidity := getStupidity(userID)
}

func PutStupidity(w http.ResponseWriter, r *http.Request) {

}
