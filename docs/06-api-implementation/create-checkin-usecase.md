# CreateCheckInUseCase

## Objetivo
Crear el Check-In semanal del empleado.

## Actor
Employee

## Preconditions
- Usuario activo.
- No existe Check-In para la semana.

## Flujo Principal
1. Crear Check-In.
2. Asociar semana.
3. Guardar borrador.

## Eventos
CheckInCreated

## Repositories
CheckInRepository

## Transacción
Sí.
