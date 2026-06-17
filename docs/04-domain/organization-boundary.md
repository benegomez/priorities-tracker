# Multi-Tenant Boundary

## Aggregate Root Principal

Organization

Todos los datos pertenecen a una organización.

## Scope

Organization
 ├─ Teams
 ├─ Users
 ├─ Projects
 ├─ Priorities
 ├─ CheckIns
 ├─ CheckOuts
 └─ CRS

## Reglas

- No cross-tenant access.
- Todas las consultas deben filtrar por organization_id.
- Toda auditoría debe incluir organization_id.
