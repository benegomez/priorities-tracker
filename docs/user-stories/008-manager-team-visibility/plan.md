---
story: 008-manager-team-visibility
status: done
branch: feature/008-manager-team-visibility
risk_level: High
complexity: L
created: 2026-07-06
---

# Plan de Implementación — US-008: Manager Team Visibility

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Backend | Módulo `teams` con 3 endpoints GET + ownership validation + tests |
| 2 | Frontend | 2 páginas (`/manager/team` + `[employeeId]`) + componentes + hooks |

**Branch único:** `feature/008-manager-team-visibility`
**Commits:** secuenciales por fase (`feat(teams):`, `feat(fe):`)
**Nota:** No hay fase de DB — `users.manager_id` ya existe.

---

## Fase 1 — Backend ✅

### 1.1 Módulo `teams` — Estructura

- [x] Crear directorios y `__init__.py`:
  - [x] `modules/teams/`
  - [x] `modules/teams/api/`
  - [x] `modules/teams/application/`
  - [x] `modules/teams/application/queries/`
  - [x] `modules/teams/infrastructure/`
  - [x] `modules/teams/infrastructure/repositories/`
  - [x] `modules/teams/tests/`
  - [x] `modules/teams/tests/unit/`

### 1.2 Repository — TeamRepositoryImpl

- [x] `modules/teams/infrastructure/repositories/team_repository_impl.py`:
  - [x] `get_direct_reports(manager_id, organization_id)` → lista de users activos
  - [x] `get_latest_crs_batch(employee_ids, organization_id)` → dict[UUID, CRS row]
  - [x] `get_week_checkins_batch(employee_ids, organization_id, week_start)` → dict[UUID, status]
  - [x] `get_week_checkouts_batch(employee_ids, organization_id, week_start)` → dict[UUID, status]
  - [x] `validate_direct_report(employee_id, manager_id, organization_id)` → Row or raise 403
  - [x] `get_checkin_for_employee(employee_id, organization_id, week_start)` → check-in row or None
  - [x] `load_priorities_with_tasks(checkin_id, organization_id)` → list of priorities with tasks

### 1.3 API — Implementación directa en router

Nota: La lógica de queries se implementó directamente en `router.py` + `team_repository_impl.py` en vez de archivos separados por query. Resultado equivalente, menos archivos.

- [x] `GET /teams/my-team` — batch queries (4 queries, no N+1)
- [x] `GET /teams/my-team/{employee_id}/crs` — reutiliza CRSRepositoryImpl
- [x] `GET /teams/my-team/{employee_id}/checkin` — reutiliza load_priorities_with_tasks

### 1.4 API — Schemas

- [x] `modules/teams/api/schemas.py` con 8 schemas Pydantic

### 1.5 API — Router

- [x] 3 endpoints GET con `require_roles("manager", "administrator")`

### 1.6 Registrar router en main.py

- [x] `teams_router` registrado con prefix `/api/v1`

### 1.7 Tests — Unit (10 passing)

- [x] `test_raises_403_for_non_report`
- [x] `test_raises_403_cross_org`
- [x] `test_returns_row_for_valid_report`
- [x] `test_returns_active_direct_reports`
- [x] `test_returns_empty_when_no_reports`
- [x] `test_returns_crs_when_available`
- [x] `test_returns_empty_dict_when_no_crs`
- [x] `test_returns_empty_for_empty_ids`
- [x] `test_returns_checkin_status`
- [x] `test_returns_empty_for_no_checkins`

### 1.8 Tests — Integration (verificado manualmente, TD-022)

- [x] GET /teams/my-team → 200 con miembros (curl)
- [x] GET /teams/my-team → 403 para employee (curl)
- [x] GET /teams/my-team/{id}/crs → 200 (curl)
- [x] GET /teams/my-team/{id}/crs → 403 cross-manager (curl)
- [x] GET /teams/my-team/{id}/checkin → 200 (curl)
- [x] GET /teams/my-team/{id}/checkin → 404 sin checkin (curl)
- [x] 401 sin token (curl)

> ⚠️ No automatizado — registrado como TD-022

### 1.9 Verificación Backend

- [x] 10 unit tests pasan
- [x] 3 endpoints responden correctamente via curl
- [x] Manager ve solo sus reportes directos
- [x] Employee recibe 403
- [x] Cross-manager access retorna 403
- [x] 401 sin token

### 1.11 Commits

```
feat(teams): add module with repository, queries, and ownership validation
feat(teams): add API router with 3 GET endpoints for team visibility
test(teams): add unit, integration, and security tests
```

---

## Fase 2 — Frontend ✅

### 2.1 Service + Types

- [x] `features/teams/services/team-service.ts` con types y 3 funciones API

### 2.2 Hooks

- [x] `useMyTeam.ts`
- [x] `useTeamMemberCRS.ts`
- [x] `useTeamMemberCheckIn.ts` (con retry=false para 404)

### 2.3 Componentes

- [x] `TeamTable.tsx` (tabla con filas inline, no componente separado TeamMemberRow)
- [x] `TeamCRSBadge.tsx`
- [x] `TeamWeekStatusBadge.tsx`
- [x] `TeamEmptyState.tsx`
- [x] `MemberCRSHistory.tsx`
- [x] `MemberCheckInView.tsx`

### 2.4 Páginas

- [x] `app/(authenticated)/manager/team/page.tsx` (reemplazó placeholder)
- [x] `app/(authenticated)/manager/team/[employeeId]/page.tsx`

### 2.5 Verificación Frontend

- [x] `npx next build --no-lint` sin errores (15 páginas)
- [x] `npm test` — 47/47 passing
- [x] `/manager/team` muestra tabla con miembros del equipo
- [x] Click en fila navega a detalle
- [x] Detalle muestra CRS historial + check-in read-only
- [x] Empty state funciona
- [x] No hay acciones de escritura

> ⚠️ Component tests no escritos — registrado como TD-023

### 2.7 Commits

```
feat(teams): add service, hooks, and team dashboard components
feat(teams): add team list and member detail pages
```

---

## Gate Final — PR

- [ ] Todos los tests pasan (unit + integration + security + component)
- [ ] Coverage >80% en módulo teams
- [ ] `npm run build` sin errores
- [ ] 3 endpoints documentados en Swagger UI
- [ ] BR-014 enforced (manager solo ve sus reportes)
- [ ] BR-016 enforced (multi-tenant)
- [ ] Security tests: 403 para employee, cross-manager, cross-org
- [ ] UI read-only (sin acciones de escritura)
- [ ] Performance: <500ms
- [ ] PR creado con resumen, nivel de riesgo High, evidencia de tests

---

## Orden de Ejecución

```
/develop-plan be    → Fase 1 (módulo teams + endpoints + tests)
/develop-plan fe    → Fase 2 (dashboard + detalle)
/git-flow pr        → PR único con las 2 fases
```
