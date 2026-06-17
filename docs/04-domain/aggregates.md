# Aggregates

## Project Aggregate

Root:
- Project

Children:
- ProjectPhase

Consistency:
- Una fase no existe sin proyecto.

## Priority Aggregate

Root:
- Priority

Children:
- Task

Consistency:
- Una tarea no existe sin prioridad.

## WeeklyCheckIn Aggregate

Root:
- WeeklyCheckIn

## WeeklyCheckOut Aggregate

Root:
- WeeklyCheckOut

## CRS Aggregate

Root:
- CommitmentReliabilityScore
