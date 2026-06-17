# Component Hierarchy

## Purpose

Define the component architecture hierarchy.

## Hierarchy Levels

Pages
→ Layouts
→ Feature Components
→ Shared Components
→ UI Components

## Layer 1 — Pages

Examples:
- EmployeeDashboardPage
- ManagerDashboardPage
- CheckInPage
- CheckOutPage
- UsersPage
- ProjectsPage

Responsibilities:
- Routing
- Data orchestration
- Feature composition

## Layer 2 — Layouts

Examples:
- AppLayout
- EmployeeLayout
- ManagerLayout
- AdminLayout

Responsibilities:
- Navigation
- Sidebar
- Header
- Breadcrumbs

## Layer 3 — Feature Components

Examples:
- CheckInWizard
- PriorityList
- CRSCard
- RiskPanel
- TeamHealthWidget

## Layer 4 — Shared Components

Examples:
- DataTable
- PageHeader
- MetricCard
- StatusBadge
- ConfirmationDialog

## Layer 5 — UI Components

Provided by shadcn/ui

Examples:
- Button
- Input
- Select
- Card
- Dialog

## Dependency Rule

Pages
→ Features
→ Shared
→ UI

Never reverse.
