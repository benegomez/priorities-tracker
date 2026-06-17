# Next.js Architecture

## Purpose
Define the technical architecture of the frontend application.

## Framework
- Next.js 15
- App Router

## Architecture Style
Feature-Based Architecture

## Application Structure
- app/
- features/
- components/
- services/
- store/
- providers/

## Rendering Strategy

### Public Pages
Static Rendering

Examples:
- Login
- Forgot Password

### Protected Pages
Dynamic Rendering

Examples:
- Dashboard
- Reports
- CRS

## Route Groups
- (auth)
- (employee)
- (manager)
- (admin)

## Layout Strategy
- RootLayout
- EmployeeLayout
- ManagerLayout
- AdminLayout

## Provider Strategy
- QueryClientProvider
- ThemeProvider
- AuthProvider
