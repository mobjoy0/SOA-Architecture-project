package httpserver

import (
	"database/sql"
	"mobjoy0/note-service/internal/handlers"
	"mobjoy0/note-service/internal/middleware"

	"github.com/go-chi/chi/v5"
)

func NewRouter(db *sql.DB) *chi.Mux {
	r := chi.NewRouter()

	noteHandler := handlers.NoteDBHandler(db)

	// Routes
	r.Route("/notes", func(r chi.Router) {
		r.Use(middleware.JWTAuthAdmin)

		r.Get("/", noteHandler.GetNotes)                                  // GET /notes?student_id=...
		r.Post("/", noteHandler.CreateNote)                               // POST /notes
		r.Delete("/", noteHandler.DeleteByFields)                         // DELETE /notes with JSON body
		r.Delete("/student/{student_id}", noteHandler.DeleteAllByStudent) // DELETE /notes/student/{id}
		r.Delete("/{id}", noteHandler.DeleteByID)                         // DELETE /notes/{id}
	})

	return r
}
