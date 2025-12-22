# Spécifications Techniques – SOA Student Management System

## 1. Introduction

This document describes the technical specifications of the SOA Student Management System. It focuses on the technical implementation, architecture, and technologies used.

## 2. Technical Architecture

The system follows a **Service-Oriented Architecture (SOA)** composed of multiple independent services implemented using different technologies and programming languages.

Communication between services is done over **HTTP** using:

* **REST** services with JSON format
* **SOAP** services with XML and WSDL contracts

An **API Gateway** is used as a centralized entry point for all client requests.

---

## 3. Global Architecture Overview

```
Client (Web / API Consumer)
        |
        v
   API Gateway 
        |
        |-------------------------------|
        v                               v
REST Services                       SOAP Services
(Étudiants, Notes, Auth)           (Cours, Paiement)
```

---

## 4. Services Technical Specifications

### 4.1 API Gateway Service

* **Technology:** Java – Spring Cloud
* **Role:** Central entry point for the system

**Responsibilities:**

* Route client requests to appropriate services
* Validate authentication tokens
* Enforce access control rules

### 4.2 Étudiants Service

* **Type:** REST
* **Technology:** Node.js – TypeScript

**Responsibilities:**

* Manage student data
* Perform CRUD operations on students

**Example Endpoints:**

```http
POST   /api/etudiants
GET    /api/etudiants/{id}
PUT    /api/etudiants/{id}
DELETE /api/etudiants/{id}
```

---

### 4.3 Cours Service

* **Type:** SOAP
* **Technology:** Python

**Responsibilities:**

* Manage course information
* Upload and download course files
* Store course files locally

---

### 4.4 Authentification Service

* **Type:** REST
* **Technology:** Java – Spring Boot

**Responsibilities:**

* Admin registration and login
* Student and professor authentication
* Generate and validate JWT tokens

---

### 4.5 Notes Service

* **Type:** REST
* **Technology:** Go (GoLang)

**Responsibilities:**

* Add student grades
* Retrieve student grades
* Delete student grades

**SOAP Operations (Example):**

```xml
addNote(etudiantId, coursId, valeur)
getNotesByEtudiant(etudiantId)
deleteNote(noteId)
```

### 4.6 Paiement Service

* **Type:** SOAP
* **Technology:** .NET

**Responsibilities:**

* Register student payments
* Check payment status

## 5. Data Formats

### REST Services

* Data format: JSON
* Communication: HTTP
* Status codes: 200, 201, 400, 401, 404, 500

### SOAP Services

* Data format: XML
* Service contracts defined using WSDL
* Error handling via SOAP Faults

## 6. Security

* Authentication using JWT tokens
* Role-based access control (Admin, Student, Professor)
* Token validation handled by the API Gateway

## 7. Deployment Strategy

* Each service is deployed independently
* Services can be developed and scaled separately
* API Gateway is the only service exposed to clients

## 8. Error Handling

* REST services return HTTP error codes
* SOAP services return SOAP Fault messages

## 9. Logging and Monitoring

* Each service logs requests and errors independently
* Logs are used for debugging and monitoring

## 10. Limitations

* No mobile application
* Local file storage for course resources
* No external payment provider integration

## 11. Conclusion

These technical specifications describe a scalable and interoperable SOA-based system combining REST and SOAP services implemented using multiple technologies.
