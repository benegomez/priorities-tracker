---
status: done
type: backend
story: docs/user-stories/006-project-phase-management/UserStory.md
depends-on: tickets/database/ticket.md
risk_level: Medium
complexity: L
---

# [BE] US-006 — Project & Phase Management API

## Objetivo

Implementar el módulo `projects` con CRUD completo de proyectos, fases y participantes. Incluye state machines, autorización por rol (admin/manager), y endpoint de fases disponibles para el PriorityForm.

## Scope

Nuevo módulo FastAPI completo. 8 endpoints. Sin UI.

## Dependencia

Ticket DB mergeado (owner_id + project_members).

---

## Endpoints

| Método | Path | Propósito | Auth |
|---|---|---|---|
| GET | /projects | Lista paginada | admin, manager |
| POST | /projects | Crear proyecto | admin, manager |
| GET | /projects/{id} | Detalle con fases + miembros | admin, manager |
| PATCH | /projects/{id} | Editar / cambiar estado | admin, manager |
| POST | /projects/{id}/phases | Crear fase | admin, manager |
| PATCH | /projects/{id}/phases/{phase_id} | Editar fase / cambiar estado | admin, manager |
| POST | /projects/{id}/members | Agregar participante | admin, manager |
| DELETE | /projects/{id}/members/{user_id} | Remover participante | admin, manager |
| GET | /projects/phases/available | Fases activas para PriorityForm | employee, manager, admin |
| GET | /users/org-members | Lista usuarios de la org (para selects) | admin, manager |

---

## Archivos a Crear

```
apps/backend/src/modules/projects/
  __init__.py
  api/
    __init__.py
    router.py               - 8 endpoints
    schemas.py              - ProjectCreate, ProjectUpdate, ProjectResponse,
                              PhaseCreate, PhaseUpdate, PhaseResponse,
                              MemberAdd, MemberResponse, AvailablePhaseItem
  application/
    __init__.py
    commands/
      __init__.py
      create_project.py
      update_project.py
      create_phase.py
      update_phase.py
      add_member.py
      remove_member.py
    queries/
      __init__.py
      list_projects.py
      get_project_detail.py
      get_available_phases.py
  domain/
    __init__.py
    entities/
      __init__.py
      project.py            - Project entity con state machine
      phase.py              - ProjectPhase entity con state machine
    repositories/
      __init__.py
      project_repository.py
  infrastructure/
    __init__.py
    repositories/
      __init__.py
      project_repository_impl.py
  tests/
    __init__.py
    unit/
      __init__.py
      test_project_use_cases.py
    integration/
      __init__.py

apps/backend/src/main.py    - MODIFY (registrar projects_router)
```

---

## State Machine Validation

### Project transitions válidas:
```python
VALID_PROJECT_TRANSITIONS = {
    "draft": ["active"],
    "active": ["on_hold", "completed"],
    "on_hold": ["active"],
    "completed": ["archived"],
    "archived": [],
}
```

### Phase transitions válidas:
```python
VALID_PHASE_TRANSITIONS = {
    "planned": ["active", "cancelled"],
    "active": ["completed", "cancelled"],
    "completed": [],
    "cancelled": [],
}
```

---

## Autorización

- `GET /projects/phases/available` → cualquier rol autenticado (employee necesita esto para PriorityForm)
- Todos los demás endpoints → solo `administrator` o `manager`
- Validar con dependency `require_roles("administrator", "manager")`

---

## Business Rules

| Regla | Validación |
|---|---|
| Solo admin/manager gestionan proyectos | Dependency de rol en router |
| owner_id debe pertenecer a la misma org | Validar en create/update |
| Participantes deben ser de la misma org | Validar en add_member |
| No duplicar participantes | Unique index + check en use case |
| Transiciones de estado válidas | Validar contra mapa de transiciones |
| Soft delete (no eliminar con prioridades activas) | Verificar antes de soft-delete |
| Multi-tenant | organization_id from JWT en todos los queries |

---

## Endpoint adicional: GET /users/org-members

Lista los usuarios activos de la organización para usar en selects de owner y participantes.

```
GET /api/v1/users/org-members
Auth: admin, manager

Response 200:
[
  { "id": "uuid", "full_name": "Employee Alpha", "role": "employee", "email": "employee@org-alpha.com" }
]
```

- Retorna solo usuarios activos (`status = 'active'`) de la misma organización
- Cualquier usuario puede ser owner (no restringido a admin/manager)
- Se usa en el frontend para poblar los selects de owner y agregar miembros

---

## Tests Requeridos

### Unit Tests

- [ ] `test_create_project_returns_draft_status`
- [ ] `test_create_project_validates_owner_same_org`
- [ ] `test_update_project_validates_state_transition`
- [ ] `test_update_project_rejects_invalid_transition`
- [ ] `test_create_phase_returns_planned_status`
- [ ] `test_update_phase_validates_state_transition`
- [ ] `test_add_member_validates_same_org`
- [ ] `test_add_member_rejects_duplicate`
- [ ] `test_employee_cannot_create_project`

### Integration Tests

- [ ] `test_endpoint_get_projects_returns_200`
- [ ] `test_endpoint_post_project_returns_201`
- [ ] `test_endpoint_get_project_detail_returns_phases_and_members`
- [ ] `test_endpoint_patch_project_changes_status`
- [ ] `test_endpoint_post_phase_returns_201`
- [ ] `test_endpoint_patch_phase_changes_status`
- [ ] `test_endpoint_post_member_returns_201`
- [ ] `test_endpoint_delete_member_returns_204`
- [ ] `test_endpoint_get_available_phases_returns_active_phases`
- [ ] `test_endpoint_returns_403_for_employee`
- [ ] `test_endpoint_get_org_members_returns_users`
- [ ] `test_endpoint_get_org_members_returns_403_for_employee`

---

## Criterios de Aceptación

- [ ] 8 endpoints implementados y respondiendo
- [ ] State machines validadas (409 en transición inválida)
- [ ] Solo admin/manager pueden gestionar (403 para employee)
- [ ] GET /projects/phases/available funciona para todos los roles
- [ ] Multi-tenant enforced en todos los queries
- [ ] Soft delete (no DELETE físico)
- [ ] Router registrado en main.py
- [ ] Tests pasan

---

## Git Branch

`feature/006-project-phase-management`
