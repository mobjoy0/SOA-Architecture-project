package models

type Note struct {
	ID        int64   `json:"id"`
	Subject   string  `json:"subject"`
	StudentID int64   `json:"student_id"`
	ExamType  string  `json:"exam_type"`
	NoteValue float64 `json:"note_value"`
}
