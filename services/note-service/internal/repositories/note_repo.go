package repositories

import (
	"database/sql"
	"mobjoy0/note-service/internal/models"
)

type NoteRepository struct {
	db *sql.DB
}

func NoteDBRepository(db *sql.DB) *NoteRepository {
	return &NoteRepository{db: db}
}

// Get all notes for a student
func (r *NoteRepository) GetAllByStudentID(studentID int64) ([]models.Note, error) {
	rows, err := r.db.Query(
		"SELECT id, subject, student_id, exam_type, note_value FROM notes WHERE student_id = ?",
		studentID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	notes := []models.Note{}
	for rows.Next() {
		var note models.Note
		if err := rows.Scan(&note.ID, &note.Subject, &note.StudentID, &note.ExamType, &note.NoteValue); err != nil {
			return nil, err
		}
		notes = append(notes, note)
	}

	return notes, nil
}

// Create a new note
func (r *NoteRepository) Create(note models.Note) error {
	_, err := r.db.Exec(
		"INSERT INTO notes (subject, student_id, exam_type, note_value) VALUES (?, ?, ?, ?)",
		note.Subject,
		note.StudentID,
		note.ExamType,
		note.NoteValue,
	)
	return err
}

// Delete a note by ID
func (r *NoteRepository) Delete(id int64) error {
	_, err := r.db.Exec("DELETE FROM notes WHERE id = ?", id)
	return err
}

// Delete by subject, exam type, and student ID
func (r *NoteRepository) DeleteBySubjectAndExamTypeAndStudentId(studentID int64, subject, examType string) error {
	_, err := r.db.Exec(
		"DELETE FROM notes WHERE student_id = ? AND subject = ? AND exam_type = ?",
		studentID, subject, examType,
	)
	return err
}

// Delete all notes for a student
func (r *NoteRepository) DeleteAllByStudentId(studentID int64) error {
	_, err := r.db.Exec(
		"DELETE FROM notes WHERE student_id = ?",
		studentID,
	)
	return err
}
