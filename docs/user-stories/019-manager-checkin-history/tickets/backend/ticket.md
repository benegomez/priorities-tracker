---
id: BE-019
us: 019-manager-checkin-history
layer: backend
status: done
risk: medium
---

# BE-019: Extender endpoint checkin con week_start opcional

## Objetivo

Agregar `week_start` como query param opcional al endpoint `GET /api/v1/teams/my-team/{employee_id}/checkin`.

## Cambio

**Archivo:** `apps/backend/src/modules/teams/api/router.py`

Endpoint actual:
```
GET /my-team/{employee_id}/checkin
→ siempre usa _get_current_week_start()
```

Endpoint modificado:
```
GET /my-team/{employee_id}/checkin?week_start=2025-06-30
→ usa week_start si se pasa, sino usa _get_current_week_start()
```

## Implementación

- Agregar `week_start: date | None = Query(None)` al handler
- Resolver: `resolved_week = week_start or _get_current_week_start()`
- Sin cambios en repositorio, schemas ni base de datos

## Acceptance Criteria

- [ ] `GET /my-team/{id}/checkin` sin params → comportamiento actual preservado
- [ ] `GET /my-team/{id}/checkin?week_start=2025-06-30` → retorna check-in de esa semana
- [ ] Si no existe check-in para esa semana → 404
- [ ] Si el empleado no es reporte directo → 403
- [ ] 3 integration tests pasando
