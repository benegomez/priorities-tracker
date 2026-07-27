---
id: 014-admin-project-management
status: completed
created: 2025-01-28
---

# Plan US-014 — Admin Project Management

## Contexto

La implementación ya existía (BE + FE). Este plan cubre únicamente los tests faltantes.
No hay migración de base de datos requerida.

## Fase 1 — Backend Tests

- [x] Crear `tests/integration/test_project_endpoints.py`
  - [x] `test_list_projects_returns_200`
  - [x] `test_status_filter`
  - [x] `test_creates_project_returns_201`
  - [x] `test_invalid_owner_returns_400`
  - [x] `test_employee_cannot_create_returns_403`
  - [x] `test_returns_detail_with_phases_and_members`
  - [x] `test_unknown_project_returns_404`
  - [x] `test_valid_transition_draft_to_active`
  - [x] `test_invalid_transition_draft_to_completed_returns_409`
  - [x] `test_create_phase_returns_201`
  - [x] `test_update_phase_valid_transition`
  - [x] `test_add_member_returns_201`
  - [x] `test_add_duplicate_member_returns_409`
- [x] Verificar que 12 unit tests existentes siguen pasando (26/26 total)

## Fase 2 — Frontend Tests

- [x] Crear `src/tests/project-management.test.tsx`
  - [x] `UserSelect renders placeholder when no value`
  - [x] `UserSelect renders user options`
  - [x] `UserSelect calls onChange when user selected`
  - [x] `UserSelect excludes ids from excludeIds prop`
  - [x] `ProjectsPage shows empty state when no projects`
  - [x] `ProjectsPage renders project list with status badge`
  - [x] `ProjectsPage shows loading skeleton when loading`
  - [x] `ProjectDetailPage renders project name and status`
  - [x] `ProjectDetailPage renders phases list`
  - [x] `ProjectDetailPage renders members list`
  - [x] `ProjectDetailPage shows loading skeleton when loading`
- [x] 98/98 tests totales pasando
- [x] Build exitoso
