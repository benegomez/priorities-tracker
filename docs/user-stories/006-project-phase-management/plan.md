---
story: 006-project-phase-management
status: pending
branch: feature/006-project-phase-management
risk_level: Medium
complexity: L
created: 2026-07-05
---

# Plan de Implementación — US-006: Project & Phase Management

## Resumen

| Fase | Ticket | Entregable |
|---|---|---|
| 1 | Database | Migración: owner_id en projects + tabla project_members |
| 2 | Backend | Módulo `projects` con 8 endpoints + state machines |
| 3 | Frontend | Páginas lista/detalle + refactor PriorityForm (cierra TD-007) |

**Branch único:** `feature/006-project-phase-management`
**Commits:** secuenciales por fase (`feat(db):`, `feat(projects):`, `feat(fe):`)

---

## Fase 1 — Database ✅

### 1.1 Migración Alembic

- [x] Crear `apps/backend/src/shared/database/migrations/202507051300_add_project_owner_and_members.py`
- [x] Implementar `upgrade()`:
  - [x] ALTER `projects` ADD COLUMN `owner_id UUID NULL REFERENCES users(id)`
  - [x] CREATE INDEX `idx_projects_owner_id`
  - [x] CREATE TABLE `project_members` con FK a organizations, projects, users
  - [x] Partial unique index `uq_project_members_project_user`
  - [x] Índices: `idx_project_members_organization_id`, `idx_project_members_project_id`, `idx_project_members_user_id`
- [x] Implementar `downgrade()`:
  - [x] DROP TABLE `project_members`
  - [x] DROP INDEX `idx_projects_owner_id`
  - [x] ALTER `projects` DROP COLUMN `owner_id`

### 1.2 Verificación

- [x] `upgrade()` ejecuta sin errores
- [x] `downgrade()` revierte completamente
- [x] Re-upgrade funciona
- [x] Unique index: insertar mismo user+project dos veces → falla
- [x] FK owner_id valida contra users

### 1.3 Commit

```
feat(db): add owner_id to projects and create project_members table
```

---

## Fase 2 — Backend ✅

### 2.10 Endpoint adicional: GET /projects/org-members

- [x] Endpoint implementado en `modules/projects/api/router.py`
- [x] Retorna usuarios activos de la organización: `[{ id, full_name, role, email }]`
- [x] Auth: admin, manager
- [x] Filtro: `status = 'active'`, `organization_id` from JWT, `deleted_at IS NULL`
- [x] Verificado via curl: retorna 3 usuarios de Org Alpha

### 2.1 Domain Entities

- [ ] `modules/projects/__init__.py` + todos los `__init__.py`
- [ ] `modules/projects/domain/entities/project.py`:
  - [ ] Dataclass con campos: id, organization_id, owner_id, name, description, status
  - [ ] `VALID_TRANSITIONS` dict
  - [ ] Método `change_status(new_status)` que valida transición
- [ ] `modules/projects/domain/entities/phase.py`:
  - [ ] Dataclass con campos: id, organization_id, project_id, name, status
  - [ ] `VALID_TRANSITIONS` dict
  - [ ] Método `change_status(new_status)` que valida transición

### 2.2 Repository

- [ ] `modules/projects/domain/repositories/project_repository.py` — ABC
- [ ] `modules/projects/infrastructure/repositories/project_repository_impl.py`:
  - [ ] `list_by_org(organization_id, status_filter, page, page_size)`
  - [ ] `get_by_id(project_id, organization_id)` — con fases y miembros
  - [ ] `save(project)`
  - [ ] `update(project)`
  - [ ] `save_phase(phase)`
  - [ ] `update_phase(phase)`
  - [ ] `add_member(organization_id, project_id, user_id)`
  - [ ] `remove_member(organization_id, project_id, user_id)`
  - [ ] `get_available_phases(organization_id)` — fases activas con project name

### 2.3 Use Cases

- [ ] `application/queries/list_projects.py` — paginado con conteos
- [ ] `application/queries/get_project_detail.py` — con fases + miembros
- [ ] `application/queries/get_available_phases.py` — para PriorityForm
- [ ] `application/commands/create_project.py`:
  - [ ] Valida owner_id pertenece a la misma org
  - [ ] Crea con status `draft`
- [ ] `application/commands/update_project.py`:
  - [ ] Valida state machine si cambia status
  - [ ] Valida owner_id si cambia
- [ ] `application/commands/create_phase.py`:
  - [ ] Valida project existe y pertenece a la org
  - [ ] Crea con status `planned`
- [ ] `application/commands/update_phase.py`:
  - [ ] Valida state machine si cambia status
- [ ] `application/commands/add_member.py`:
  - [ ] Valida user pertenece a la misma org
  - [ ] Valida no duplicado
- [ ] `application/commands/remove_member.py`:
  - [ ] Soft delete del membership

### 2.4 API

- [ ] `modules/projects/api/schemas.py`:
  - [ ] `ProjectCreate` — `{ name, description?, owner_id }`
  - [ ] `ProjectUpdate` — `{ name?, description?, owner_id?, status? }`
  - [ ] `ProjectListItem` — `{ id, name, description, status, owner, phases_count, members_count }`
  - [ ] `ProjectListResponse` — `{ items[], total, page, page_size }`
  - [ ] `ProjectDetailResponse` — `{ id, name, description, status, owner, phases[], members[] }`
  - [ ] `PhaseCreate` — `{ name }`
  - [ ] `PhaseUpdate` — `{ name?, status? }`
  - [ ] `PhaseResponse` — `{ id, name, status }`
  - [ ] `MemberAdd` — `{ user_id }`
  - [ ] `MemberResponse` — `{ id, user_id, full_name, role }`
  - [ ] `AvailablePhaseItem` — `{ id, name, project_name }`

- [ ] `modules/projects/api/router.py`:
  - [ ] `GET /projects` — list (admin, manager)
  - [ ] `POST /projects/` — create (admin, manager)
  - [ ] `GET /projects/phases/available` — available phases (all roles)
  - [ ] `GET /projects/{id}` — detail (admin, manager)
  - [ ] `PATCH /projects/{id}` — update (admin, manager)
  - [ ] `POST /projects/{id}/phases/` — create phase (admin, manager)
  - [ ] `PATCH /projects/{id}/phases/{phase_id}` — update phase (admin, manager)
  - [ ] `POST /projects/{id}/members/` — add member (admin, manager)
  - [ ] `DELETE /projects/{id}/members/{user_id}` — remove member (admin, manager)
  - [ ] Role check dependency en todos excepto `available`

### 2.5 Registrar router en main.py

- [ ] Importar y registrar `projects_router` con prefix `/api/v1`

### 2.6 Tests — Unit

- [ ] `test_create_project_returns_draft_status`
- [ ] `test_create_project_validates_owner_same_org`
- [ ] `test_update_project_validates_state_transition`
- [ ] `test_update_project_rejects_invalid_transition`
- [ ] `test_create_phase_returns_planned_status`
- [ ] `test_update_phase_validates_state_transition`
- [ ] `test_add_member_validates_same_org`
- [ ] `test_add_member_rejects_duplicate`
- [ ] `test_project_state_machine_valid_transitions`
- [ ] `test_phase_state_machine_valid_transitions`

### 2.7 Tests — Integration

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

### 2.8 Verificación Backend

- [ ] Todos los tests pasan
- [ ] 8 endpoints responden correctamente
- [ ] State machines enforced (409 en transición inválida)
- [ ] Solo admin/manager pueden gestionar (403 para employee)
- [ ] GET /projects/phases/available funciona para employee
- [ ] Multi-tenant enforced

### 2.9 Commits

```
feat(projects): add domain entities with state machines
feat(projects): add repository, use cases, and API router (8 endpoints)
test(projects): add unit and integration tests
```

---

## Fase 3 — Frontend ✅

### 3.10 User Select Component

- [x] Crear `features/projects/hooks/useOrgMembers.ts`:
  - [x] `useQuery(["users", "org-members"])` → `GET /api/v1/projects/org-members`
- [x] Crear `features/projects/components/UserSelect.tsx`:
  - [x] Select dropdown con opciones: `Nombre Completo (rol)`
  - [x] Soporta `excludeIds` para filtrar miembros ya agregados

### 3.11 Refactor ProjectForm (owner)

- [x] Páginas de lista (`/admin/projects`, `/manager/projects`):
  - [x] Input de texto reemplazado por `UserSelect` para owner
  - [x] Muestra todos los usuarios activos de la org

### 3.12 Refactor MemberAddForm (participantes)

- [x] Páginas de detalle (`/admin/projects/[id]`, `/manager/projects/[id]`):
  - [x] Input de texto reemplazado por `UserSelect`
  - [x] Filtra usuarios que ya son miembros (`excludeIds`)
  - [x] Al seleccionar, agrega inmediatamente

### 3.13 Owner editable en detalle

- [x] Responsable se muestra como `UserSelect` en la vista de detalle
- [x] Al cambiar, se envía `PATCH /projects/{id}` con nuevo `owner_id`

### 3.14 Páginas de manager

- [x] `/manager/projects` — lista de proyectos con crear
- [x] `/manager/projects/[id]` — detalle con fases, miembros, owner editable
- [x] `/manager/team` — placeholder
- [x] `/manager/weekly` — placeholder

### 3.15 Hydration fix

- [x] `(authenticated)/layout.tsx` lee rol de cookie via `useEffect` (evita hydration mismatch)

### 3.16 Verificación

- [x] `npm run build` sin errores (13 páginas)
- [x] `npm test` — 47/47 passing
- [x] Owner se selecciona de dropdown (crear + editar)
- [x] Participantes se agregan de dropdown (filtra existentes)
- [x] Manager ve y gestiona proyectos correctamente
- [x] MOCK_PHASES eliminado, PriorityForm usa datos reales

### 3.1 Service + Schemas + Hooks

- [ ] `features/projects/services/project-service.ts` — 9 funciones API
- [ ] `features/projects/schemas/project-schema.ts` — Zod schemas
- [ ] Hooks:
  - [ ] `useProjects` — useQuery lista paginada
  - [ ] `useProjectDetail` — useQuery detalle
  - [ ] `useCreateProject` — useMutation
  - [ ] `useUpdateProject` — useMutation
  - [ ] `useCreatePhase` — useMutation
  - [ ] `useUpdatePhase` — useMutation
  - [ ] `useAddMember` — useMutation
  - [ ] `useRemoveMember` — useMutation
  - [ ] `useAvailablePhases` — useQuery (para PriorityForm)

### 3.2 Componentes

- [ ] `ProjectList.tsx` — lista de ProjectCards
- [ ] `ProjectCard.tsx` — card con nombre, estado, owner, conteos
- [ ] `ProjectForm.tsx` — crear/editar proyecto (nombre, descripción, owner select)
- [ ] `ProjectDetail.tsx` — vista detalle completa
- [ ] `PhaseList.tsx` — lista de fases inline con estado
- [ ] `PhaseForm.tsx` — crear/editar fase (nombre)
- [ ] `PhaseStatusSelect.tsx` — dropdown de transiciones válidas
- [ ] `MemberList.tsx` — lista de participantes con botón remover
- [ ] `MemberAddForm.tsx` — select de usuarios + botón agregar
- [ ] `ProjectStatusBar.tsx` — barra visual de estado con transiciones

### 3.3 Páginas

- [ ] `app/(authenticated)/admin/projects/page.tsx` — lista de proyectos
- [ ] `app/(authenticated)/admin/projects/[id]/page.tsx` — detalle proyecto
- [ ] `app/(authenticated)/manager/projects/page.tsx` — misma vista (reutiliza componentes)

### 3.4 Refactor PriorityForm (cierra TD-007)

- [ ] Crear `features/priorities/hooks/useAvailablePhases.ts`:
  - [ ] Llama a `GET /projects/phases/available`
  - [ ] Retorna `{ id, name, project_name }[]`
- [ ] Modificar `PriorityForm.tsx`:
  - [ ] Usar `useAvailablePhases()` en vez de prop `phases`
  - [ ] Remover prop `phases` del componente
- [ ] Modificar `app/(authenticated)/employee/checkin/page.tsx`:
  - [ ] Eliminar `MOCK_PHASES` constante
  - [ ] No pasar `phases` a PriorityForm

### 3.5 Navegación

- [ ] Agregar "Proyectos" al menú admin en `config/navigation.ts`
- [ ] Agregar "Proyectos del Equipo" al menú manager (ya existe, verificar href)

### 3.6 Tests

- [ ] `test_ProjectList_renders_project_cards`
- [ ] `test_ProjectCard_shows_name_status_owner`
- [ ] `test_ProjectForm_validates_required_fields`
- [ ] `test_PhaseList_renders_phases_with_status`
- [ ] `test_MemberList_renders_members`
- [ ] `test_ProjectStatusBar_shows_valid_transitions`
- [ ] `test_PriorityForm_uses_available_phases_hook`
- [ ] `test_available_phases_hook_fetches_from_api`

### 3.7 Verificación Frontend

- [ ] `npm run build` sin errores
- [ ] `npm test` — todos los tests pasan
- [ ] Lista de proyectos funcional
- [ ] Detalle con fases y miembros funcional
- [ ] State machine enforced en UI
- [ ] PriorityForm usa datos reales (MOCK_PHASES eliminado)
- [ ] Responsive verificado
- [ ] TD-007 cerrado

### 3.8 Commits

```
feat(projects): add service, schemas, hooks, and components
feat(projects): add project list and detail pages
feat(priorities): replace MOCK_PHASES with useAvailablePhases (closes TD-007)
test(fe): add component tests for project management
```

---

## Gate Final — PR

- [ ] Todos los tests pasan (backend + frontend)
- [ ] `npm run build` sin errores
- [ ] 8 endpoints documentados en Swagger UI
- [ ] State machines enforced en BE y FE
- [ ] Solo admin/manager pueden gestionar proyectos
- [ ] PriorityForm usa datos reales
- [ ] MOCK_PHASES eliminado del código
- [ ] TD-007 marcado como closed en technical-debt.md
- [ ] PR creado con resumen y evidencia

---

## Orden de Ejecución

```
/develop-plan db    → Fase 1 (migración)
/develop-plan be    → Fase 2 (módulo projects)
/develop-plan fe    → Fase 3 (UI + refactor PriorityForm)
/git-flow pr        → PR único con las 3 fases
```
