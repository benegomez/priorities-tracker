# Authorization UI Strategy

## Purpose
Define role-based UI visibility.

## Roles

- Administrator
- Manager
- Employee

## Employee Access

Allowed:
- Own Dashboard
- Check-In
- Check-Out
- History

Restricted:
- Administration
- Other Employees

## Manager Access

Allowed:
- Team Dashboard
- CRS
- Reports
- AI Insights

Restricted:
- Administration

## Administrator Access

Allowed:
- Users
- Teams
- Projects
- Phases
- Settings

## UI Authorization

Unauthorized actions are hidden, not disabled.

## Navigation Authorization

Menus rendered dynamically by role.
