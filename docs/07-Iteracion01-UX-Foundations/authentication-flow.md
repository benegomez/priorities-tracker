# Authentication Flow

## Authentication Method

JWT + Refresh Token

## Login Flow

Login
→ Backend Validation
→ Access Token
→ Refresh Token
→ Authenticated Session

## Session Flow

Request
→ Access Token
→ API
→ Response

## Refresh Flow

Expired Token
→ Refresh Token
→ New Access Token

## Logout Flow

Logout
→ Revoke Session
→ Clear Cookies
→ Redirect Login

## Authentication Guard

Protected routes require authenticated users.
