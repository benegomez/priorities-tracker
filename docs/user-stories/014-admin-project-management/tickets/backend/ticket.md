---
status: pending
type: backend
story: docs/user-stories/014-admin-project-management/UserStory.md
risk_level: Medium
complexity: S
---

# [BE] US-014 — Admin Project Management Tests

## Objetivo

Agregar tests de integración para el módulo `projects`. La implementación ya existe — este ticket cubre únicamente la cobertura de tests faltante.

## Contexto

El módulo `projects` tiene:
- 9 endpoints implementados en `api/router.py`
- Schemas en `api/schemas.py`
- Entidades de dominio con máquinas de estado en `domain/entities/`
- 12 unit tests pasando en `tests/unit/test_project_use_cases.py`
- **0 integration tests** — `tests/integration/` está vacío

## Scope

Solo crear `tests/integration/test_project_endpoints.py`. No modificar código existente.

---

## Archivo a Crear

```
apps/backend/src/modules/projects/tests/integration/
  test_project_endpoints.py
```

---

## Tests de Integración Requeridos (10 tests)

### Proyectos CRUD
- `test_list_projects_returns_200` — GET /api/v1/projects retorna 200 con items
- `test_create_project_returns_201` — POST crea proyecto en estado draft
- `test_create_project_invalid_owner_returns_400` — owner de otra org → 400
- `test_get_project_detail_returns_phases_and_members` — GET /{id} incluye fases y miembros
- `test_update_project_valid_transition_returns_200` — PATCH draft→active → 200
- `test_update_project_invalid_transition_returns_409` — PATCH draft→completed → 409

### Fases
- `test_create_phase_returns_201` — POST /{id}/phases crea fase en estado planned
- `test_update_phase_valid_transition` — PATCH planned→active → 200

### Miembros
- `test_add_member_returns_201` — POST /{id}/members agrega participante
- `test_add_duplicate_member_returns_409` — mismo user_id → 409

### RBAC
- `test_employee_cannot_create_project_returns_403` — rol employee → 403

---

## Patrón de Tests (igual que teams)

```python
# httpx.AsyncClient directo contra localhost:8000
# _TOKEN_CACHE para evitar rate limiter
# Crear recursos propios en cada test (no depender de seeds)
```

---

## Criterios de Aceptación

- [ ] 10+ integration tests pasando
- [ ] Tests existentes (12 unit) siguen pasando
- [ ] Cobertura >80% en router.py
