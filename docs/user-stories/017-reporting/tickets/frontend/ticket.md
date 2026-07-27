---
status: pending
type: frontend
story: docs/user-stories/017-reporting/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Medium
complexity: L
---

# [FE] US-017 — Reporting: Frontend Pages

## Objetivo

Implementar 3 páginas de reporte consumiendo los nuevos endpoints del módulo `reporting`.

## Archivos a Crear

```
apps/frontend/src/
  features/reports/
    services/
      report-service.ts         # getIndividualReport, getTeamReport, getProjectReport
    hooks/
      useIndividualReport.ts
      useTeamReport.ts
      useProjectReport.ts
    components/
      ReportWeeklyBreakdown.tsx  # tabla de breakdown semanal (reutilizable)
      ReportStatCard.tsx         # tarjeta de métrica (reutilizable)
  app/(authenticated)/
    employee/
      reports/
        page.tsx                 # /employee/reports — reporte individual
    manager/
      reports/
        page.tsx                 # /manager/reports — reporte de equipo
        project/
          [id]/
            page.tsx             # /manager/reports/project/[id] — reporte de proyecto
  tests/
    reporting.test.tsx           # 6 tests de componentes
```

## Componentes

### ReportStatCard
Props: `{ label: string, value: string | number, sublabel?: string }`
Muestra una métrica destacada (ej. "Tasa de cumplimiento: 83%")

### ReportWeeklyBreakdown
Props: `{ rows: WeeklyBreakdownRow[] }`
Tabla con columnas: Semana | Comprometidas | Completadas | Arrastradas | CRS

### /employee/reports
- Carga `useIndividualReport`
- Muestra: `ReportStatCard` × 3 (total, completadas, tasa) + `ReportWeeklyBreakdown`

### /manager/reports
- Carga `useTeamReport`
- Muestra: stats del equipo + tabla de miembros con completion_rate y CRS

### /manager/reports/project/[id]
- Carga `useProjectReport(id)`
- Muestra: stats del proyecto + tabla de fases con completion_rate

## Tests Requeridos (6 tests)

- `ReportStatCard renders label and value`
- `ReportWeeklyBreakdown renders table rows`
- `ReportWeeklyBreakdown shows empty state`
- `EmployeeReportsPage shows loading skeleton`
- `EmployeeReportsPage renders stats when data loaded`
- `ManagerReportsPage shows empty state when no team members`

## Criterios de Aceptación

- [ ] 3 páginas de reporte implementadas y navegables
- [ ] `ReportStatCard` y `ReportWeeklyBreakdown` reutilizables
- [ ] 6 tests pasando
- [ ] 116+ tests totales frontend pasando
- [ ] Build exitoso
