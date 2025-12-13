package main

import (
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"

	"mobjoy0/note-service/internal/database"
	"mobjoy0/note-service/internal/httpserver"
)

func main() {
	// Load .env first
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found, using environment variables")
	}

	db := database.Connect("database/notes.db")
	defer db.Close()

	database.InitSchema(db)

	router := httpserver.NewRouter(db)

	port := os.Getenv("PORT")
	if port == "" {
		port = "5050"
	}

	log.Println("Server running on port:", port)
	log.Fatal(http.ListenAndServe(":"+port, router))
}
