---
id: 014-admin-project-management
status: pending
created: 2025-01-28
---

# Plan US-014 — Admin Project Management

## Contexto

La implementación ya existe (BE + FE). Este plan cubre únicamente los tests faltantes.
No hay migración de base de datos requerida.

## Fase 1 — Backend Tests

- [ ] Crear `tests/integration/test_project_endpoints.py`
  - [ ] `test_list_projects_returns_200`
  - [ ] `test_create_project_returns_201`
  - [ ] `test_create_project_invalid_owner_returns_400`
  - [ ] `test_get_project_detail_returns_phases_and_members`
  - [ ] `test_update_project_valid_transition_returns_200`
  - [ ] `test_update_project_invalid_transition_returns_409`
  - [ ] `test_create_phase_returns_201`
  - [ ] `test_update_phase_valid_transition`
  - [ ] `test_add_member_returns_201`
  - [ ] `test_add_duplicate_member_returns_409`
  - [ ] `test_employee_cannot_create_project_returns_403`
- [ ] Verificar que 12 unit tests existentes siguen pasando

## Fase 2 — Frontend Tests

- [ ] Crear `src/tests/project-management.test.tsx`
  - [ ] `UserSelect renders placeholder when no value`
  - [ ] `UserSelect renders user options`
  - [ ] `UserSelect calls onChange when user selected`
  - [ ] `ProjectsPage shows empty state when no projects`
  - [ ] `ProjectsPage renders project list with status badge`
  - [ ] `ProjectDetailPage renders project name and status`
  - [ ] `ProjectDetailPage renders phases list`
  - [ ] `ProjectDetailPage renders members list`
- [ ] Verificar 87+ tests totales pasando
- [ ] Verificar build `npx next build --no-lint`
