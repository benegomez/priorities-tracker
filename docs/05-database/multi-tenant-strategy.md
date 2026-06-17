# Multi Tenant Strategy

## Modelo Seleccionado

Shared Database
Shared Schema
Tenant Column

## Tenant Key

organization_id

## Reglas

Toda tabla de negocio contiene organization_id.

Toda consulta filtra organization_id.

No existe acceso cross-tenant.

## Beneficios

Menor costo.
Mayor simplicidad.
Escalabilidad suficiente para MVP.
