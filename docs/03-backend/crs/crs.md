# CRS Module (Versión Extendida)

## Estado: ✅ Implementado (US-007)

## Objetivo
El Commitment Reliability Score (CRS) es el principal diferenciador de Priorities Tracker.
Mide la capacidad de una persona para cumplir consistentemente los compromisos que ella misma define.

## Principios
- Basado en compromisos autoasignados.
- Transparente.
- Auditable (`formula_version = "v1.0"` almacenado con cada score).
- Comparable en el tiempo.
- No reemplaza la evaluación humana.

## Entradas (Implementadas)
- Prioridades comprometidas (count del check-in).
- Prioridades completadas (marcadas en check-out).
- Tareas comprometidas (count del check-in).
- Tareas completadas (marcadas en check-out).
- Arrastres (prioridades con status `carried_over`).
- Historial de scores previos (promedio para tendencia).

## Salidas (Implementadas)
- CRS semanal (score 0–100).
- Tendencia (`improving`, `stable`, `declining`).
- Nivel de riesgo (`low`, `moderate`, `high`).

## Endpoints
- `GET /api/v1/crs/current` — Score actual
- `GET /api/v1/crs/history` — Historial

## Reportes (Futuro)
- Individual ✅ (dashboard implementado).
- Equipo (pendiente).
- Proyecto (pendiente).
- Fase de Proyecto (pendiente).
