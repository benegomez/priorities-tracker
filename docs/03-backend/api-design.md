# API Design

## Objetivo

Definir los estándares para el diseño de APIs REST del backend.

## Principios

- REST First
- Versionado explícito
- Contratos estables
- OpenAPI como fuente de verdad

## Estructura

/api/v1/

### Recursos principales

/auth
/users
/teams
/projects
/project-phases
/priorities
/tasks
/checkins
/checkouts
/crs
/reports

## Convenciones

- GET lectura
- POST creación
- PUT actualización completa
- PATCH actualización parcial
- DELETE eliminación lógica

## Respuestas

{
  "data": {},
  "metadata": {},
  "errors": []
}

## Seguridad

JWT + RBAC
