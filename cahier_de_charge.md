# Cahier des Charges – SOA Student Management System

## 1. Project Overview
The project aims to design and implement a Service-Oriented Architecture (SOA)
combining REST and SOAP web services to manage a student information system.

## 2. Objectives
- Apply SOA principles
- Implement REST and SOAP services
- Ensure interoperability between services
- Secure access using authentication

## 3. Architecture
The system is composed of independent services communicating over HTTP:

- REST services (JSON)
- SOAP services (XML)

## 4. Services Description

### 4.1 Étudiants Service (REST)
- CRUD operations on students

### 4.2 Cours Service (REST)
- Implemented in Python
- Uses local storage for course files

### 4.3 Authentification Service (REST)
- Admin registration and login
- Student and professor authentication

### 4.4 Notes Service (SOAP) 
- Add and retrieve student grades
- Delete student grades

### 4.5 Paiement Service (SOAP) 
- Register student payments
- Check payment status

### 4.6 API Gateway Service (REST)
- Acts as a single entry point for all clients
- Routes requests to the appropriate internal services
- Handles authentication and authorization
- Improves security and simplifies client communication

## 5. Non-Functional Requirements
- Secure communication
- Data consistency
- Service independence
- Scalability

## 6. Technologies Used

| Service | Type | Language / Technology |
|-------|------|----------------------|
| API Gateway | REST | Java – Spring Boot |
| Étudiants Service | REST | Nodejs Typescript |
| Cours Service | REST | Python |
| Authentification Service | REST | Spring Boot |
| Notes Service | SOAP | GoLang |
| Paiement Service | SOAP | .NET |


## 7. Deliverables
- Source code of all services
- WSDL files for SOAP services
- API documentation for REST services
- Presentation
