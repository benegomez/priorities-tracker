# Frontend Security

## Authentication

JWT Access Token
Refresh Token

## Token Storage

Recommended:

HTTP Only Cookies

## Authorization

RBAC

Roles:

- Administrator
- Manager
- Employee

## Route Protection

Protected routes require authentication.

## Role Protection

/admin/*

Requires Administrator role.

## API Security

All requests include Bearer Token.

## Frontend Security Controls

- Session expiration handling
- Unauthorized redirects
- CSRF protection
- XSS prevention
- Secure cookie configuration

## Security Events

Log:

- Login
- Logout
- Session Expiration
- Authorization Failures
