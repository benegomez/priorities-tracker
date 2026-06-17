# SubmitCheckInUseCase

## Objetivo
Enviar el Check-In semanal.

## Reglas
- Debe existir al menos una prioridad.
- Toda prioridad pertenece a una fase.
- Jerarquía:
Project -> Phase -> Priority -> Task

## Eventos
CheckInSubmitted

## Servicios
PlanningCycleService
