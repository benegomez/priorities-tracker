# Teams Module

## Estado: ✅ Parcialmente Implementado (US-008)

## Objetivo
Gestionar equipos y relaciones manager-colaborador. Proveer visibilidad al manager sobre el estado de su equipo.

## Responsabilidades Implementadas (US-008)
- Consultar reportes directos del manager (via `users.manager_id`)
- Mostrar CRS actual y estado semanal (check-in/check-out) de cada miembro
- Consultar historial CRS de un miembro específico
- Consultar check-in semanal de un miembro (read-only)

## Responsabilidades Futuras
- Crear equipos
- Asignar miembros
- Definir managers

## Endpoints Implementados

| Método | Path | Descripción |
|---|---|---|
| GET | `/api/v1/teams/my-team` | Reportes directos con CRS + week status |
| GET | `/api/v1/teams/my-team/{id}/crs` | Historial CRS de un miembro |
| GET | `/api/v1/teams/my-team/{id}/checkin` | Check-in semanal de un miembro (read-only) |

## Seguridad
- Solo roles `manager` y `administrator` (BR-014)
- Validación de ownership: 403 si employee_id no es reporte directo
- Multi-tenant: organization_id del JWT (BR-016)

## Estructura del Módulo

```
modules/teams/
├── api/
│   ├── router.py          (3 GET endpoints)
│   └── schemas.py         (8 schemas Pydantic)
├── infrastructure/
│   └── repositories/
│       └── team_repository_impl.py  (7 métodos, batch queries)
└── tests/unit/
    └── test_team_queries.py  (10 tests)
```

## Performance
- 4 queries batch (no N+1) para la vista principal
- <500ms para equipos de hasta 15 personas
