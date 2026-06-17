# Domain Model (Deep Dive)

## Core Domain
- Check-In
- Check-Out
- Commitment Reliability Score (CRS)

## Dominio Central

Proyecto
  ↓
Fase Proyecto
  ↓
Prioridad
  ↓
Tarea

## Relaciones

Organization
 └─ Teams
     └─ Users
         └─ Weekly CheckIns
         └─ Weekly CheckOuts

Project
 └─ ProjectPhase
      └─ Priority
           └─ Task

## Aggregate Boundaries

Project Aggregate
Priority Aggregate
Weekly Planning Aggregate
Weekly Execution Aggregate
CRS Aggregate

## Domain Services

- CommitmentScoringService
- RiskDetectionService
- PriorityContinuationService
