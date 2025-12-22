package handlers

import (
	"database/sql"
	"encoding/json"
	"mobjoy0/note-service/internal/models"
	"mobjoy0/note-service/internal/repositories"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
)

type NoteHandler struct {
	repo *repositories.NoteRepository
}

func NoteDBHandler(db *sql.DB) *NoteHandler {
	return &NoteHandler{
		repo: repositories.NoteDBRepository(db),
	}
}

// GET /notes?student_id=123
func (h *NoteHandler) GetNotes(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json")
	studentIDStr := r.URL.Query().Get("student_id")

	if studentIDStr == "" {
		http.Error(w, "student_id required", http.StatusBadRequest)
		return
	}
	studentID, _ := strconv.ParseInt(studentIDStr, 10, 64)

	notes, err := h.repo.GetAllByStudentID(studentID)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(notes)
}

// POST /notes
func (h *NoteHandler) CreateNote(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var note models.Note

	if err := json.NewDecoder(r.Body).Decode(&note); err != nil {
		http.Error(w, "Invalid JSON: "+err.Error(), http.StatusBadRequest)
		return
	}

	if note.NoteValue < 0 || note.NoteValue > 20 {
		http.Error(w, "NoteValue must be between 0 and 20", http.StatusBadRequest)
		return
	}

	if err := h.repo.Create(note); err != nil {
		http.Error(w, "Failed to create note: "+err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(note)
}

// DELETE /notes/{id}
func (h *NoteHandler) DeleteByID(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	idStr := chi.URLParam(r, "id")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	h.repo.Delete(id)
	w.WriteHeader(http.StatusNoContent)
}

// DELETE /notes (JSON body)
func (h *NoteHandler) DeleteByFields(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json")
	var req struct {
		StudentID int64  `json:"student_id"`
		Subject   string `json:"subject"`
		ExamType  string `json:"exam_type"`
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	h.repo.DeleteBySubjectAndExamTypeAndStudentId(req.StudentID, req.Subject, req.ExamType)
	w.WriteHeader(http.StatusNoContent)
}

// DELETE /notes/student/{student_id}
func (h *NoteHandler) DeleteAllByStudent(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	studentIDStr := chi.URLParam(r, "student_id")
	studentID, _ := strconv.ParseInt(studentIDStr, 10, 64)
	h.repo.DeleteAllByStudentId(studentID)
	w.WriteHeader(http.StatusNoContent)
}
