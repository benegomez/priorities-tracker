---
story: docs/user-stories/016-manager-individual-view/UserStory.md
status: pending
---

# Plan — US-016 Manager Individual View

## Contexto

La implementación ya existe. Esta US agrega cobertura de tests para formalizar la funcionalidad.

## Phase 1 — Backend Tests (`/develop-plan be`)

**Archivo:** `apps/backend/src/modules/teams/tests/integration/test_team_member_detail_endpoints.py`

- 5 integration tests para `GET /teams/my-team/{id}/crs`
- Patrón: `httpx.AsyncClient` + `_TOKEN_CACHE`

## Phase 2 — Frontend Tests (`/develop-plan fe`)

**Archivo:** `apps/frontend/src/tests/manager-individual.test.tsx`

- 5 component tests para `MemberCRSHistory`, `MemberCheckInView`, `TeamMemberDetailPage`
- Patrón: `vi.mock` + `QueryClientProvider`
