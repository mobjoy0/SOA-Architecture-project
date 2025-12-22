import sqlite3
from datetime import datetime

DB_NAME = "../courses.db"


def init_db():
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
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses WHERE filename = ?", (filename,))
    course = cursor.fetchone()
    conn.close()

    return dict(course) if course else None


def get_all_courses():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses ORDER BY upload_date DESC")
    courses = cursor.fetchall()
    conn.close()

    return [dict(course) for course in courses]


def get_courses_by_subject(subject):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses WHERE subject = ? ORDER BY upload_date DESC", (subject,))
    courses = cursor.fetchall()
    conn.close()

    return [dict(course) for course in courses]
