---
status: pending
type: backend
story: docs/user-stories/013-admin-team-management/UserStory.md
depends-on: tickets/database/ticket.md
risk_level: Medium
complexity: M
---

# [BE] US-013 — Admin Team Management API

## Objetivo

Extender el módulo `teams` con 6 endpoints REST de administración que permiten al administrador gestionar equipos: listar, crear, ver detalle con miembros, editar, asignar y remover miembros.

## Scope

Módulo `teams` existente — se agregan capas `domain/` y `application/` faltantes, nuevos endpoints en `router.py`, nuevo repositorio de administración. Los endpoints existentes (`/my-team`, `/my-team/{id}/crs`, `/my-team/{id}/checkin`) no se modifican.

---

## FR de Referencia

- FR-007 — Create teams
- FR-008 — Edit teams
- FR-009 — Assign employees to teams

## Business Rules Aplicables

- **BR-NEW-05** — Nombre de equipo único por organización → `409`
- **BR-NEW-06** — Manager del equipo debe tener rol `manager` o `administrator` → `400`
- **BR-NEW-07** — Usuario solo puede pertenecer a un equipo (asignar remueve del anterior)
- **BR-NEW-08** — No se puede eliminar equipo con miembros activos
- **BR-016** — Multi-tenant: `organization_id` del JWT
- **BR-017** — Todos los aggregates pertenecen a una organización

---

## Contrato API

### GET /api/v1/teams
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Query params | `page=1`, `page_size=20` |
| Response 200 | `TeamListResponse` (paginado) |

### POST /api/v1/teams
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Request body | `TeamCreate` |
| Response 201 | `TeamResponse` |
| Response 409 | Nombre duplicado en la organización |
| Response 400 | manager_id con rol inválido |
| Response 404 | manager_id no existe |

### GET /api/v1/teams/{id}
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Response 200 | `TeamDetailResponse` (incluye lista de miembros) |
| Response 404 | Equipo no existe en la organización |

### PATCH /api/v1/teams/{id}
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Request body | `TeamUpdate` (todos opcionales) |
| Response 200 | `TeamResponse` |
| Response 409 | Nombre duplicado |
| Response 404 | Equipo no existe |

### POST /api/v1/teams/{id}/members
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Request body | `TeamMemberAdd` |
| Response 200 | `TeamMemberResponse` |
| Response 404 | Usuario no existe en la organización |
| Response 409 | Usuario ya es miembro de este equipo |

### DELETE /api/v1/teams/{id}/members/{user_id}
| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: administrator) |
| Response 204 | No Content |
| Response 404 | Usuario no es miembro del equipo |

---

## Schemas Pydantic

```python
class TeamCreate(BaseModel):
    name: str          # max 200
    manager_id: UUID | None = None

class TeamUpdate(BaseModel):
    name: str | None = None
    manager_id: UUID | None = None

class TeamMemberAdd(BaseModel):
    user_id: UUID

class TeamMemberItem(BaseModel):  # reutilizar nombre distinto al existente
    id: UUID
    first_name: str
    last_name: str
    role: str
    status: str

class TeamResponse(BaseModel):
    id: UUID
    name: str
    manager_id: UUID | None
    manager_name: str | None
    member_count: int
    created_at: datetime
    updated_at: datetime

class TeamDetailResponse(TeamResponse):
    members: list[TeamMemberItem]

class TeamListResponse(BaseModel):
    items: list[TeamResponse]
    total: int
    page: int
    page_size: int
    pages: int

class TeamMemberResponse(BaseModel):
    team_id: UUID
    user_id: UUID
```

---

## Archivos a Crear / Modificar

```
apps/backend/src/modules/teams/
  domain/
    __init__.py
    entities/
      __init__.py
      team.py                          # TeamDetail dataclass
    repositories/
      __init__.py
      team_admin_repository.py         # interface abstracta
  application/
    commands/
      __init__.py
      create_team.py                   # CreateTeamCommand + UseCase
      update_team.py                   # UpdateTeamCommand + UseCase
      manage_members.py                # AddMemberCommand + RemoveMemberCommand + UseCases
  infrastructure/
    repositories/
      team_admin_repo_impl.py          # SQLAlchemy impl (raw SQL)
  api/
    schemas.py                         # MODIFY — agregar nuevos schemas (no tocar existentes)
    router.py                          # MODIFY — agregar 6 endpoints nuevos (no tocar existentes)
  tests/
    unit/
      test_team_admin.py               # nuevos unit tests
    integration/
      __init__.py
      test_team_admin_endpoints.py     # integration tests
```

---

## Queries principales (TeamAdminRepoImpl)

```sql
-- GET list
SELECT t.id, t.name, t.manager_id, t.organization_id, t.created_at, t.updated_at,
       u.first_name || ' ' || u.last_name AS manager_name,
       COUNT(m.id) FILTER (WHERE m.deleted_at IS NULL) AS member_count
FROM teams t
LEFT JOIN users u ON t.manager_id = u.id AND u.deleted_at IS NULL
LEFT JOIN users m ON m.team_id = t.id AND m.deleted_at IS NULL
WHERE t.organization_id = :org_id AND t.deleted_at IS NULL
GROUP BY t.id, u.first_name, u.last_name
ORDER BY t.name
LIMIT :limit OFFSET :offset

-- GET detail members
SELECT id, first_name, last_name, role, status
FROM users
WHERE team_id = :team_id AND organization_id = :org_id AND deleted_at IS NULL
ORDER BY first_name, last_name

-- POST members (assign — BR-NEW-07: limpia equipo anterior automáticamente)
UPDATE users SET team_id = :team_id, updated_at = now()
WHERE id = :user_id AND organization_id = :org_id AND deleted_at IS NULL

-- DELETE members (remove)
UPDATE users SET team_id = NULL, updated_at = now()
WHERE id = :user_id AND team_id = :team_id AND organization_id = :org_id AND deleted_at IS NULL
```

---

## Tests Requeridos

### Unit Tests (test_team_admin.py)

- [ ] `test_create_team_raises_409_on_duplicate_name`
- [ ] `test_create_team_raises_400_on_invalid_manager_role`
- [ ] `test_create_team_raises_404_on_missing_manager`
- [ ] `test_update_team_raises_409_on_duplicate_name`
- [ ] `test_add_member_raises_409_on_already_member`
- [ ] `test_add_member_removes_from_previous_team`
- [ ] `test_remove_member_raises_404_when_not_member`

### Integration Tests (test_team_admin_endpoints.py)

- [ ] `test_get_teams_returns_paginated_list`
- [ ] `test_post_team_creates_and_returns_201`
- [ ] `test_post_team_returns_409_on_duplicate_name`
- [ ] `test_get_team_detail_includes_members`
- [ ] `test_patch_team_updates_name`
- [ ] `test_post_member_assigns_user_to_team`
- [ ] `test_delete_member_removes_user_from_team`
- [ ] `test_employee_gets_403_on_all_endpoints`
- [ ] `test_manager_gets_403_on_all_endpoints`

---

## Criterios de Aceptación

- [ ] `GET /api/v1/teams` retorna lista paginada con `member_count` y `manager_name`
- [ ] `POST /api/v1/teams` crea equipo, `409` en nombre duplicado
- [ ] `GET /api/v1/teams/{id}` retorna detalle con lista de miembros
- [ ] `PATCH /api/v1/teams/{id}` actualiza parcialmente
- [ ] `POST /api/v1/teams/{id}/members` asigna usuario, limpia equipo anterior (BR-NEW-07)
- [ ] `DELETE /api/v1/teams/{id}/members/{user_id}` remueve usuario, retorna `204`
- [ ] `403` para roles `employee` y `manager`
- [ ] Endpoints existentes (`/my-team`, etc.) no se modifican ni rompen
- [ ] `organization_id` nunca aceptado del body
- [ ] Tests pasan

---

## Git Branch

`feature/013-admin-team-management`
