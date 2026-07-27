---
id: 013-admin-team-management
status: in-progress
created: 2025-01-28
---

# Plan US-013 — Admin Team Management

## Fase 1 — Base de Datos

- [ ] Crear migración `202501280900_create_teams_add_team_id_to_users.py`
  - [ ] `upgrade()`: CREATE TABLE teams + ALTER TABLE users ADD COLUMN team_id
  - [ ] `downgrade()`: DROP COLUMN team_id + DROP TABLE teams
- [ ] Ejecutar `alembic upgrade head` en contenedor
- [ ] Verificar schema en DB

## Fase 2 — Backend

- [ ] Crear estructura de capas faltantes en módulo `teams`
  - [ ] `domain/entities/team.py` — TeamDetail dataclass
  - [ ] `domain/repositories/team_admin_repository.py` — interface abstracta
  - [ ] `application/commands/create_team.py` — CreateTeamUseCase (BR-NEW-05, BR-NEW-06)
  - [ ] `application/commands/update_team.py` — UpdateTeamUseCase
  - [ ] `application/commands/manage_members.py` — AddMemberUseCase + RemoveMemberUseCase (BR-NEW-07)
  - [ ] `infrastructure/repositories/team_admin_repo_impl.py` — SQLAlchemy impl
- [ ] Agregar schemas en `api/schemas.py` (sin tocar schemas existentes)
- [ ] Agregar 6 endpoints en `api/router.py` (sin tocar endpoints existentes)
- [ ] Unit tests — `tests/unit/test_team_admin.py` (7 tests)
- [ ] Integration tests — `tests/integration/test_team_admin_endpoints.py` (9 tests)
- [ ] Verificar que tests existentes (`test_team_queries.py`) siguen pasando

## Fase 3 — Frontend

- [ ] Agregar tipos y funciones admin en `features/teams/services/team-service.ts`
- [ ] Crear `features/teams/hooks/useAdminTeams.ts` (6 hooks)
- [ ] Crear `features/teams/components/AdminTeamTable.tsx`
- [ ] Crear `features/teams/components/TeamFormModal.tsx`
- [ ] Crear `features/teams/components/TeamMembersModal.tsx`
- [ ] Crear `app/(authenticated)/admin/teams/page.tsx`
- [ ] Agregar entrada en `config/navigation.ts`
- [ ] Tests — `tests/team-management.test.tsx` (7 tests)
- [ ] Verificar build `npx next build --no-lint`
