# Soft Delete Strategy

## Campos Estándar
- deleted_at TIMESTAMPTZ NULL
- deleted_by UUID NULL

## Regla
Nunca eliminar registros funcionales de negocio.
