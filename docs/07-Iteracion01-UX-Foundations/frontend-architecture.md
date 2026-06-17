# Frontend Architecture

## Purpose

Define the overall frontend architecture for Priorities Tracker.

## Technology Stack

### Framework
Next.js 15

### Language
TypeScript

### UI
shadcn/ui

### Styling
TailwindCSS

### Data Fetching
TanStack Query

### Local State
Zustand

## Architecture Style

Feature-Based Architecture

Application
→ Features
→ Components
→ Services
→ API

## Frontend Layers

### Presentation Layer
Pages and UI Components

### Feature Layer
Business-specific modules

Examples:
- checkins
- priorities
- projects
- teams
- crs

### API Layer
Communication with backend services

### Shared Layer
Reusable functionality

## Architectural Goals

- Scalability
- Maintainability
- Testability
- Performance
- Accessibility
