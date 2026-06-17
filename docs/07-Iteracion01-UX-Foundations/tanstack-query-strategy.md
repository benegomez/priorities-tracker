# TanStack Query Strategy

## Purpose
Define server-state management.

## Query Ownership
Each feature owns its own queries.

Examples:
- priorities
- projects
- teams
- crs

## Query Keys

- ['priorities']
- ['priorities', id]
- ['projects']
- ['crs', employeeId]

## Stale Time

### Static Data
5 minutes

Examples:
- Projects
- Phases

### Operational Data
30 seconds

Examples:
- Priorities
- Tasks

### Dashboard Data
60 seconds

## Mutation Strategy
All mutations invalidate related queries after success.

## Prefetching
Use route-based prefetching.
