# Business Rules (Deep Dive)

## Planificación

BR-001 Un empleado sólo puede tener un Check-In por semana.
BR-002 Un empleado sólo puede tener un Check-Out por semana.
BR-003 Una prioridad debe pertenecer a una fase.
BR-004 Una fase debe pertenecer a un proyecto.
BR-005 Una tarea debe pertenecer a una prioridad.

## Ejecución

BR-006 Una prioridad puede continuar a la siguiente semana.
BR-007 Las tareas completadas no se copian automáticamente.
BR-008 No puede cerrarse una prioridad inexistente.

## CRS

BR-009 El CRS es calculado automáticamente.
BR-010 El CRS no puede modificarse manualmente.
BR-011 Toda ejecución CRS debe ser auditable.
BR-012 El CRS se recalcula cuando existe Check-Out.

## Seguridad

BR-013 Un empleado sólo ve sus prioridades.
BR-014 Un manager sólo ve sus equipos.
BR-015 Un administrador puede ver toda la organización.

## Multi-Tenant

BR-016 Ningún usuario puede acceder a datos de otra organización.
BR-017 Todos los agregados pertenecen a una organización.
