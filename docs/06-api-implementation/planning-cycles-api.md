# Planning Cycles API

## WeeklyPlanningCycle

Vista agregada semanal.

GET /api/v1/planning-cycles/{week}

Respuesta conceptual:

{
  "week": "2026-W25",
  "checkin": {},
  "priorities": [],
  "tasks": [],
  "checkout": {},
  "crs": {}
}

GET /api/v1/planning-cycles/current

GET /api/v1/planning-cycles/team/{week}

Beneficios:

- Dashboard simplificado
- Reporting unificado
- Vista semanal consolidada
