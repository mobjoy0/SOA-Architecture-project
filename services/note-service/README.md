# Note Service API

A simple REST API for managing student notes (marks) using Go, Chi, and SQLite. All endpoints are **protected by JWT**, and only users with **role=ADMIN** can access them.

---

## Base URL

```
http://localhost:5050
```

---

## Authentication

All endpoints require a **JWT token** in the `Authorization` header:

```
Authorization: Bearer <token>
```

The JWT must contain `"role": "ADMIN"`.

---

## Endpoints

### 1. GET `/notes?student_id=<id>`

Retrieve all notes for a specific student.

**Request**

```
GET /notes?student_id=123
Authorization: Bearer <token>
```

**Response (200 OK)**

```json
[
  {
    "id": 1,
    "student_id": 123,
    "subject": "Math",
    "exam_type": "Midterm",
    "note_value": 17.5,
    "created_at": "2025-12-13T18:00:00Z"
  },
  {
    "id": 2,
    "student_id": 123,
    "subject": "Physics",
    "exam_type": "Final",
    "note_value": 15.0,
    "created_at": "2025-12-13T18:05:00Z"
  }
]
```

**Errors**

* `400 Bad Request` – if `student_id` query param is missing
* `401 Unauthorized` – if JWT is missing or invalid
* `403 Forbidden` – if user is not ADMIN

---

### 2. POST `/notes`

Create a new note.

**Request**

```
POST /notes
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "student_id": 123,
  "subject": "Math",
  "exam_type": "Midterm",
  "note_value": 17.5
}
```

**Response (200 OK)**

```json
{
  "id": 3,
  "student_id": 123,
  "subject": "Math",
  "exam_type": "Midterm",
  "note_value": 17.5,
  "created_at": "2025-12-13T18:10:00Z"
}
```

---

### 3. DELETE `/notes/{id}`

Delete a note by its ID.

**Request**

```
DELETE /notes/3
Authorization: Bearer <token>
```

**Response**

* `204 No Content` – note deleted successfully

---

### 4. DELETE `/notes` (JSON body)

Delete a note by student, subject, and exam type.

**Request**

```
DELETE /notes
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "student_id": 123,
  "subject": "Math",
  "exam_type": "Midterm"
}
```

**Response**

* `204 No Content` – note deleted successfully

---

### 5. DELETE `/notes/student/{student_id}`

Delete all notes for a student.

**Request**

```
DELETE /notes/student/123
Authorization: Bearer <token>
```

**Response**

* `204 No Content` – all notes for the student deleted successfully

---

## Notes

* `note_value` is a decimal (REAL) representing the student’s mark.
* All endpoints return **JSON**.
* Only users with **role=ADMIN** can access the API.
* All timestamps are in **UTC**.
