# Auth Service – API Documentation

## Base Path

`/auth`

---

## Register User

**Endpoint**
`POST /auth/register`

**Request Body**

```json
{
  "username": "admin",
  "email": "admin@admin.admin",
  "password": "password123",
  "role": "ADMIN"
}
```

**Success Response (200)**

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@admin.admin"
}
```

---

## Login User

**Endpoint**
`POST /auth/login`

**Request Body**

```json
{
  "username": "admin",
  "password": "password123"
}
```

**Success Response (200)**

```json
{
  "token": "JWT_TOKEN_HERE"
}
```

**Error Response (401)**

```json
{
  "error": "Invalid credentials"
}
```

---

## Delete User (Admin Only)

**Endpoint**
`DELETE /auth/delete/{id}`

**Headers**

```
Authorization: Bearer <JWT_TOKEN>
```

**Path Variable**

* `id` — ID of the user to delete

**Success Response (200)**

```json
{
  "message": "User deleted successfully"
}
```

**Forbidden (403)**

```json
{
  "error": "Access denied"
}
```

**Not Found (404)**

```json
{
  "error": "User not found"
}
```

---

## JWT Token Payload

```json
{
  "role": "ADMIN",
  "id": 1,
  "email": "admin@admin.admin",
  "sub": "admin",
  "iat": 1765586389,
  "exp": 1765596265
}
```

---

## Authorization Rules

* Only users with `role = ADMIN` can delete users
* JWT must be sent in the `Authorization` header using the format:

```
Authorization: Bearer <token>
```
