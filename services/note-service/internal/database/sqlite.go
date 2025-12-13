package database

import (
	"database/sql"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

func Connect(path string) *sql.DB {
	db, err := sql.Open("sqlite3", path)
	if err != nil {
		log.Fatal(err)
	}

	if err := db.Ping(); err != nil {
		log.Fatal(err)
	}

	return db
}

func InitSchema(db *sql.DB) {
	query := `
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
		student_id INTEGER,
		exam_type TEXT NOT NULL,
        subject TEXT NOT NULL,
		note_value REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    `
	if _, err := db.Exec(query); err != nil {
		log.Fatal(err)
	}
}
