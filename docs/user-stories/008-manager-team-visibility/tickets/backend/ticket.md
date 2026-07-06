---
status: done
type: backend
story: docs/user-stories/008-manager-team-visibility/UserStory.md
depends-on: null
risk_level: High
complexity: L
---

# [BE] US-008 — Manager Team Visibility API

## Objetivo

Implementar 3 endpoints read-only que permiten al manager consultar el estado de su equipo: lista de reportes directos con CRS y estado semanal, historial CRS de un empleado, y check-in semanal de un empleado.

## Scope

Nuevo módulo `teams` con router, schemas, queries. Sin modificaciones a tablas existentes. Solo endpoints GET (read-only).

---

## FR de Referencia

- FR-026 — Team Dashboard
- FR-027 — Weekly View
- FR-028 — Individual View
- FR-033 — CRS History

## Business Rules Aplicables

- **BR-014** — Manager solo ve sus reportes directos (`WHERE manager_id = current_user.id`)
- **BR-016** — Multi-tenant (`AND organization_id = :org_id` del JWT)
- **BR-017** — Todos los agregados pertenecen a una organización
- **NUEVA** — Solo usuarios con `status = 'active'` aparecen en la lista
- **NUEVA** — 403 si employee_id no es reporte directo (no revelar existencia)

---

## Contrato API

### GET /api/v1/teams/my-team

| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: manager, administrator) |
| operation_id | `get_my_team` |
| Response 200 | TeamOverviewResponse |
| Response 403 | Insufficient permissions (employee role) |

### GET /api/v1/teams/my-team/{employee_id}/crs

| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: manager, administrator) |
| operation_id | `get_team_member_crs` |
| Path params | `employee_id` (UUID) |
| Query params | `weeks` (default 8, max 52) |
| Response 200 | TeamMemberCRSResponse |
| Response 403 | Employee is not a direct report |

### GET /api/v1/teams/my-team/{employee_id}/checkin

| Campo | Valor |
|---|---|
| Auth | Bearer JWT (role: manager, administrator) |
| operation_id | `get_team_member_checkin` |
| Path params | `employee_id` (UUID) |
| Response 200 | CheckInResponse (same schema as GET /checkins/current) |
| Response 403 | Employee is not a direct report |
| Response 404 | No check-in for current week |

---

## Archivos a Crear / Modificar

```
apps/backend/src/modules/teams/
  __init__.py
  api/
    __init__.py
    router.py               - 3 endpoints GET
    schemas.py              - TeamOverviewResponse, TeamMemberItem, TeamMemberCRSResponse, etc.
  application/
    __init__.py
    queries/
      __init__.py
      get_my_team.py        - GetMyTeamQuery
      get_member_crs.py     - GetTeamMemberCRSQuery
      get_member_checkin.py - GetTeamMemberCheckInQuery
  infrastructure/
    __init__.py
    repositories/
      __init__.py
      team_repository_impl.py - Queries para reportes directos + aggregation
  tests/
    __init__.py
    unit/
      __init__.py
      test_team_queries.py
    integration/
      __init__.py

apps/backend/src/main.py    - MODIFY (registrar teams_router)
```

---

## Schemas Pydantic

```python
class TeamMemberCRS(BaseModel):
    score: float
    trend: str
    risk_level: str

class TeamMemberWeekStatus(BaseModel):
    week_start: date
    checkin_status: str | None   # "draft" | "submitted" | None
    checkout_status: str | None  # "draft" | "submitted" | None

class TeamMemberItem(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    crs: TeamMemberCRS | None
    week_status: TeamMemberWeekStatus

class TeamOverviewResponse(BaseModel):
    members: list[TeamMemberItem]

class TeamMemberEmployee(BaseModel):
    id: UUID
    first_name: str
    last_name: str

class TeamMemberCRSCurrent(BaseModel):
    score: float
    trend: str
    risk_level: str
    week_start: date

class CRSHistoryItem(BaseModel):
    week_start: date
    score: float
    trend: str
    risk_level: str

class TeamMemberCRSResponse(BaseModel):
    employee: TeamMemberEmployee
    current: TeamMemberCRSCurrent | None
    history: list[CRSHistoryItem]
```

Para el endpoint de checkin, reutilizar `CheckInResponse` del módulo `checkin`.

---

## Queries de Implementación

### GetMyTeamQuery

```sql
-- 1. Obtener reportes directos activos
SELECT id, first_name, last_name, email
FROM users
WHERE manager_id = :manager_id
  AND organization_id = :org_id
  AND status = 'active'
  AND deleted_at IS NULL
ORDER BY first_name, last_name;

-- 2. Para cada miembro, obtener CRS más reciente (batch)
SELECT DISTINCT ON (employee_id) employee_id, score, trend, risk_level
FROM crs_scores
WHERE employee_id = ANY(:member_ids)
  AND organization_id = :org_id
  AND deleted_at IS NULL
ORDER BY employee_id, week_start DESC;

-- 3. Para cada miembro, obtener check-in/check-out de la semana (batch)
SELECT employee_id, status AS checkin_status
FROM check_ins
WHERE employee_id = ANY(:member_ids)
  AND organization_id = :org_id
  AND week_start = :current_week_start
  AND deleted_at IS NULL;

SELECT employee_id, status AS checkout_status
FROM check_outs
WHERE employee_id = ANY(:member_ids)
  AND organization_id = :org_id
  AND week_start = :current_week_start
  AND deleted_at IS NULL;
```

**Performance:** 4 queries totales (no N+1). Para equipos de hasta 15 personas esto es <50ms.

### Validación de ownership (shared helper)

```python
async def validate_direct_report(
    session: AsyncSession,
    employee_id: UUID,
    manager_id: UUID,
    organization_id: UUID,
) -> Row:
    """Returns user row if valid direct report, raises 403 otherwise."""
    result = await session.execute(
        text("""
            SELECT id, first_name, last_name FROM users
            WHERE id = :employee_id
              AND manager_id = :manager_id
              AND organization_id = :org_id
              AND deleted_at IS NULL
        """),
        {"employee_id": employee_id, "manager_id": manager_id, "org_id": organization_id},
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=403, detail="Employee is not a direct report")
    return row
```

### GetTeamMemberCRSQuery

1. Validar ownership (helper)
2. Reutilizar `CRSRepositoryImpl.get_latest_by_employee()` para current
3. Reutilizar `CRSRepositoryImpl.get_history()` para history

### GetTeamMemberCheckInQuery

1. Validar ownership (helper)
2. Buscar check-in de la semana actual para el employee_id
3. Cargar prioridades con tareas (reutilizar lógica de `_load_priorities_with_tasks`)

---

## Reutilización de Código Existente

| Componente | Ubicación actual | Uso en US-008 |
|---|---|---|
| `CRSRepositoryImpl.get_latest_by_employee()` | `modules/crs/infrastructure/` | CRS actual del miembro |
| `CRSRepositoryImpl.get_history()` | `modules/crs/infrastructure/` | Historial CRS del miembro |
| `_load_priorities_with_tasks()` | `modules/checkin/api/router.py` | Check-in del miembro |
| `require_roles()` | `modules/auth/api/dependencies.py` | Auth en los 3 endpoints |
| `get_current_week_start()` | lógica en checkin/checkout | Calcular semana actual |

**Nota:** `_load_priorities_with_tasks` es una función privada del router de checkin. Opciones:
1. Extraerla a un servicio compartido en `shared/` (preferido)
2. Duplicar la lógica en el módulo teams (aceptable si es simple)

Decisión: **Opción 2** — la lógica es una query SQL directa, duplicar es más simple que crear una dependencia cross-module.

---

## Tests Requeridos

> Nivel de riesgo: High → Unit + Integration + Security

### Unit Tests

- [ ] `test_get_my_team_returns_active_direct_reports`
- [ ] `test_get_my_team_excludes_inactive_users`
- [ ] `test_get_my_team_returns_empty_when_no_reports`
- [ ] `test_get_my_team_includes_crs_when_available`
- [ ] `test_get_my_team_returns_null_crs_when_none`
- [ ] `test_get_my_team_includes_week_status`
- [ ] `test_validate_direct_report_raises_403_for_non_report`
- [ ] `test_validate_direct_report_raises_403_cross_org`
- [ ] `test_get_member_crs_returns_current_and_history`
- [ ] `test_get_member_crs_returns_null_current_when_no_crs`

### Integration Tests

- [ ] `test_endpoint_get_my_team_returns_200_with_members`
- [ ] `test_endpoint_get_my_team_returns_200_empty_for_no_reports`
- [ ] `test_endpoint_get_my_team_returns_403_for_employee`
- [ ] `test_endpoint_get_member_crs_returns_200`
- [ ] `test_endpoint_get_member_crs_returns_403_non_report`
- [ ] `test_endpoint_get_member_checkin_returns_200`
- [ ] `test_endpoint_get_member_checkin_returns_404_no_checkin`
- [ ] `test_endpoint_get_member_checkin_returns_403_non_report`

### Security Tests

- [ ] `test_all_endpoints_return_401_without_token`
- [ ] `test_all_endpoints_return_403_for_employee_role`
- [ ] `test_cross_manager_access_returns_403`
- [ ] `test_cross_org_access_returns_403`

---

## Criterios de Aceptación

- [ ] GET /teams/my-team retorna reportes directos con CRS y week status
- [ ] GET /teams/my-team/{id}/crs retorna historial CRS del empleado
- [ ] GET /teams/my-team/{id}/checkin retorna check-in con prioridades/tareas
- [ ] Solo roles manager/administrator pueden acceder (403 para employee)
- [ ] Manager solo ve sus propios reportes directos (BR-014)
- [ ] Multi-tenant enforced (BR-016)
- [ ] Empleados inactivos no aparecen en la lista
- [ ] 403 (no 404) cuando employee_id no es reporte directo
- [ ] Performance: <500ms para equipo de 15 personas
- [ ] Tests de seguridad pasan

---

## Git Branch

`feature/008-manager-team-visibility`
