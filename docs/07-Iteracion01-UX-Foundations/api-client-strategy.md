# API Client Strategy

## Purpose

Define frontend-backend communication.

## Communication Model

Frontend
→ API Client
→ REST API
→ Backend

## HTTP Client

Recommended:
Axios

## API Modules

- auth
- users
- teams
- projects
- priorities
- tasks
- checkins
- checkouts
- crs
- reports
- ai

## Error Handling

Normalized structure:

{
  "code": "VALIDATION_ERROR",
  "message": "Priority name is required"
}

## Query Caching

Managed through:
TanStack Query

## Retry Strategy

GET → Retry

POST → No Retry
