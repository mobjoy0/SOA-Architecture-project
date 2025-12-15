import sqlite3
from datetime import datetime

DB_NAME = "../courses.db"


def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            subject TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_course(user_id, filename, file_path, subject):
    """Add a course file record to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO courses (user_id, filename, file_path, subject)
        VALUES (?, ?, ?, ?)
    """, (user_id, filename, file_path, subject))

    conn.commit()
    course_id = cursor.lastrowid
    conn.close()

    return course_id


def get_course_by_filename(filename):
    """Get course record by filename."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses WHERE filename = ?", (filename,))
    course = cursor.fetchone()
    conn.close()

    return dict(course) if course else None


def get_all_courses():
    """Get all course records."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses ORDER BY upload_date DESC")
    courses = cursor.fetchall()
    conn.close()

    return [dict(course) for course in courses]


def get_courses_by_subject(subject):
    """Get all courses for a specific subject."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses WHERE subject = ? ORDER BY upload_date DESC", (subject,))
    courses = cursor.fetchall()
    conn.close()

    return [dict(course) for course in courses]
