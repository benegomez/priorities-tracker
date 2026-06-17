# Performance Considerations

## Objetivos

- Respuesta < 300 ms para operaciones comunes.
- Dashboards < 2 segundos.

## Estrategias

### PostgreSQL
- Índices compuestos.
- EXPLAIN ANALYZE.

### Redis
- Cache de dashboards.
- Cache CRS.

### Reporting
- Queries optimizadas.
- Agregaciones precalculadas futuras.

## Observabilidad

Medir:
- Query latency.
- Slow queries.
- Cache hit ratio.
