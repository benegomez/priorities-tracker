# State Management

## Philosophy

Server state and client state should remain separated.

## Server State

Managed with:

TanStack Query

Examples:
- Priorities
- Projects
- Teams
- CRS
- Reports

## Client State

Managed with:

Zustand

Examples:
- Sidebar
- Theme
- Filters
- Wizard Progress

## Avoid

Global business state.

Business data should remain in query caches.

## Query Structure

Examples:

- usePriorities()
- useProjects()
- useCRS()

## Mutation Structure

Examples:

- createPriority()
- updatePriority()
- submitCheckIn()
