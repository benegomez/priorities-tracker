# CRS Engine

## Responsabilidad

Servicio de dominio encargado del cálculo del CRS.

## Casos de Uso

- CalculateCRSUseCase
- RecalculateCRSUseCase
- GenerateTrendUseCase

## Flujo

CheckIn
  ↓
CheckOut
  ↓
CRS Engine
  ↓
Score
  ↓
Reporting

## Reglas

- No editable manualmente.
- Recalculable.
- Versionado.
