---
story: docs/user-stories/017-reporting/UserStory.md
status: done
completed: 2025-01-28
pr: "#17"
merge_commit: 23dd6bc
---

# Plan — US-017 Reporting

## Contexto

Implementación completa del módulo `reporting`. No existe ni en backend ni en frontend.

## Phase 1 — Backend (`/develop-plan be`)

1. Crear estructura del módulo `reporting` (Clean Architecture)
2. Implementar `ReportingRepositoryImpl` con 3 queries de agregación SQL
3. Implementar 3 query handlers (`IndividualReportQuery`, `TeamReportQuery`, `ProjectReportQuery`)
4. Implementar `router.py` con 3 endpoints GET + schemas Pydantic
5. Registrar router en `main.py`
6. Crear 6 integration tests

## Phase 2 — Frontend (`/develop-plan fe`)

1. Crear `features/reports/` con service, hooks y 2 componentes reutilizables
2. Implementar `/employee/reports/page.tsx`
3. Implementar `/manager/reports/page.tsx`
4. Implementar `/manager/reports/project/[id]/page.tsx`
5. Crear 6 component tests
