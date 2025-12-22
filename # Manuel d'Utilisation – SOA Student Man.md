USER MANUAL – SOA STUDENT MANAGEMENT SYSTEM

1. Introduction
This document explains how to use the student management system based on a Service-Oriented Architecture (SOA). It covers access to REST and SOAP services, usage of the API Gateway, and the main features available for different user roles.

2. Prerequisites
- Modern web browser or API tool (Postman, Insomnia)
- Internet connection
- User account (Admin, Student, Professor)
- SOAP tools (if using Grades or Payment Service, e.g., SoapUI)

3. System Access
All requests go through the API Gateway.
Base URL: http://localhost:8888
REST endpoints: JSON format
SOAP endpoints: XML format via WSDL

4. Student Service (REST)
Features: CRUD operations for students

Request examples:
POST /students
PUT /students/{id}
GET /students/{id}
DELETE /students/{id}

Notes:
- Admin users can create, update, and delete students.
- Students can view their information but cannot modify it.

5. Course Service (SOAP)
Features: Course management, upload/download, retrieval

Request examples:
POST /courses/upload
GET /courses/download/{id}
GET /courses

Notes:
- Professors can upload course materials.
- Students can download available courses.

6. Authentication Service (REST)
Features: Login and registration

Examples:
POST /auth/register (admin only)
POST /auth/login

Notes:
- A JWT token is required to access REST services.
- Admin users create and manage user accounts.

7. Grades Service (SOAP)
Features: Add, view, and delete grades

SOAP operation examples:
addGrade(studentId, courseId, value)
getGradesByStudent(studentId)
deleteGrade(gradeId)

Notes:
- Accessible via SOAP tools (e.g., SoapUI)
- Mainly used by professors for grade management.

8. Payment Service (SOAP)
Features: Register payments and check payment status

SOAP operation examples:
payFees(studentId, amount)
getPaymentStatus(studentId)

Notes:
- Accessible via SOAP tools
- Students and administration can verify payment status.

9. API Gateway Usage
- All requests are routed through the gateway
- JWT tokens are validated before accessing services
- Simplifies access to REST and SOAP services

10. Best Practices
- Always include the JWT token in REST request headers
- Check WSDL files before sending SOAP requests
- Refer to technical documentation to understand parameters
- Do not modify data without proper authorization
