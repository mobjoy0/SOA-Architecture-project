# Course Management API Documentation

## REST API Endpoints

**Base URL:** `http://localhost:5001`

### 1. Upload Course (Admin/Professor Only)

**Endpoint:** `POST /upload`

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: multipart/form-data
```

**Request Body:**
```
file: <PDF file>
subject: <string>
```

**Example (cURL):**
```bash
curl -X POST http://localhost:5001/upload \
  -H "Authorization: Bearer eyJhbGc..." \
  -F "file=@course.pdf" \
  -F "subject=Mathematics"
```

**Success Response (201):**
```json
{
  "message": "File 'course.pdf' uploaded successfully",
  "course_id": 1,
  "subject": "Mathematics"
}
```

**Error Responses:**
- **401 Unauthorized:**
```json
{
  "error": "Missing or invalid token"
}
```
- **403 Forbidden:**
```json
{
  "error": "Forbidden: You do not have permission to upload"
}
```
- **400 Bad Request:**
```json
{
  "error": "Subject is required"
}
```

---

### 2. Download Course (All Authenticated Users)

**Endpoint:** `GET /download/<filename>`

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```

**Example (cURL):**
```bash
curl -X GET http://localhost:5001/download/course.pdf \
  -H "Authorization: Bearer eyJhbGc..." \
  -O
```

**Success Response (200):**
- Returns PDF file as download

**Error Responses:**
- **401 Unauthorized:**
```json
{
  "error": "Missing or invalid token"
}
```
- **403 Forbidden:**
```json
{
  "error": "Unauthorized"
}
```
- **404 Not Found:**
```json
{
  "error": "File not found"
}
```

---

### 3. List All Courses (All Authenticated Users)

**Endpoint:** `GET /courses`

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters (Optional):**
- `subject` - Filter by subject

**Example (cURL):**
```bash
# Get all courses
curl -X GET http://localhost:5001/courses \
  -H "Authorization: Bearer eyJhbGc..."

# Filter by subject
curl -X GET http://localhost:5001/courses?subject=Mathematics \
  -H "Authorization: Bearer eyJhbGc..."
```

**Success Response (200):**
```json
{
  "courses": [
    {
      "id": 1,
      "user_id": "user123",
      "filename": "course.pdf",
      "file_path": "../courses/course.pdf",
      "subject": "Mathematics",
      "upload_date": "2024-12-15 10:30:00"
    },
    {
      "id": 2,
      "user_id": "user456",
      "filename": "physics.pdf",
      "file_path": "../courses/physics.pdf",
      "subject": "Physics",
      "upload_date": "2024-12-14 09:15:00"
    }
  ]
}
```

**Error Responses:**
- **401 Unauthorized:**
```json
{
  "error": "Missing or invalid token"
}
```
- **403 Forbidden:**
```json
{
  "error": "Unauthorized"
}
```

---

## SOAP API Endpoints

**Base URL:** `http://localhost:8000`

**WSDL:** `http://localhost:8000/soap?wsdl`

**Service Endpoint:** `http://localhost:8000/soap_service`

### 1. List All Courses

**Operation:** `listCourses`

**Request (SOAP Envelope):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope 
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:sch="school.course.soap">
   <soapenv:Header/>
   <soapenv:Body>
      <sch:listCourses/>
   </soapenv:Body>
</soapenv:Envelope>
```

**Example (cURL):**
```bash
curl -X POST http://localhost:8000/soap_service \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sch="school.course.soap">
   <soapenv:Header/>
   <soapenv:Body>
      <sch:listCourses/>
   </soapenv:Body>
</soapenv:Envelope>'
```

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope 
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:tns="school.course.soap">
   <soapenv:Body>
      <tns:listCoursesResponse>
         <tns:listCoursesResult>
            <tns:Course>
               <tns:id>1</tns:id>
               <tns:user_id>user123</tns:user_id>
               <tns:filename>course.pdf</tns:filename>
               <tns:file_path>../courses/course.pdf</tns:file_path>
               <tns:subject>Mathematics</tns:subject>
               <tns:upload_date>2024-12-15 10:30:00</tns:upload_date>
            </tns:Course>
            <tns:Course>
               <tns:id>2</tns:id>
               <tns:user_id>user456</tns:user_id>
               <tns:filename>physics.pdf</tns:filename>
               <tns:file_path>../courses/physics.pdf</tns:file_path>
               <tns:subject>Physics</tns:subject>
               <tns:upload_date>2024-12-14 09:15:00</tns:upload_date>
            </tns:Course>
         </tns:listCoursesResult>
      </tns:listCoursesResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

### 2. Get Course File (Base64 Encoded)

**Operation:** `getCourse`

**Request (SOAP Envelope):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope 
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:sch="school.course.soap">
   <soapenv:Header/>
   <soapenv:Body>
      <sch:getCourse>
         <sch:filename>course.pdf</sch:filename>
      </sch:getCourse>
   </soapenv:Body>
</soapenv:Envelope>
```

**Example (cURL):**
```bash
curl -X POST http://localhost:8000/soap_service \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sch="school.course.soap">
   <soapenv:Header/>
   <soapenv:Body>
      <sch:getCourse>
         <sch:filename>course.pdf</sch:filename>
      </sch:getCourse>
   </soapenv:Body>
</soapenv:Envelope>'
```

**Success Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope 
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:tns="school.course.soap">
   <soapenv:Body>
      <tns:getCourseResponse>
         <tns:getCourseResult>JVBERi0xLjQKJeLjz9MKMyAwIG9iag...</tns:getCourseResult>
      </tns:getCourseResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

**Error Response (File Not Found):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope 
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:tns="school.course.soap">
   <soapenv:Body>
      <tns:getCourseResponse>
         <tns:getCourseResult>File not found</tns:getCourseResult>
      </tns:getCourseResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

---

## Authentication

REST API endpoints require JWT authentication with the following roles:
- **ADMIN** - Can upload and download courses
- **PROFESSOR** - Can upload and download courses  
- **Any authenticated user** - Can download and list courses

JWT token should be included in the `Authorization` header:
```
Authorization: Bearer <your_jwt_token>
```

SOAP API endpoints do **not** require authentication (for educational purposes only).