# Routing Strategy

## Framework

- Next.js 15
- App Router

## Public Routes

/auth/login
/auth/forgot-password
/auth/reset-password

## Employee Routes

/employee
/employee/checkin
/employee/checkout
/employee/priorities
/employee/tasks
/employee/history
/employee/profile

## Manager Routes

/manager
/manager/team
/manager/team/[employeeId]
/manager/reports
/manager/crs
/manager/ai-insights

## Administration Routes

/admin
/admin/users
/admin/users/[id]
/admin/teams
/admin/teams/[id]
/admin/projects
/admin/projects/[id]
/admin/phases
/admin/settings

## Route Protection

- Public
- Authenticated
- Role-Based Access Control (RBAC)
