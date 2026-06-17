# Testing Strategy

## Objetivo

Garantizar calidad y mantenibilidad.

## Pirámide de Pruebas

### Unit Tests

Cobertura mínima 70%.

### Integration Tests

Validar interacción módulos.

### API Tests

Validar contratos REST.

### E2E Tests

Flujos críticos.

## Casos Prioritarios

- Check-In
- Check-Out
- CRS
- Reporting

## Herramientas

- Pytest
- HTTPX
- Factory Boy

## CI/CD

Toda Pull Request debe ejecutar:

- Unit Tests
- Integration Tests
- Linting
