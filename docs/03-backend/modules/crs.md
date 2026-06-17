
# CRS Module

## Objetivo

Implementar el Commitment Reliability Score (CRS).

Es el principal diferenciador estratégico de Priorities Tracker.

---

# Definición

El CRS mide la confiabilidad de una persona para cumplir los compromisos que ella misma definió.

---

# Factores Evaluados

## Prioridades

- Comprometidas
- Completadas

## Tareas

- Comprometidas
- Completadas

## Continuidad

- Arrastres
- Frecuencia de arrastre

## Consistencia

- Semanas consecutivas
- Tendencia histórica

---

# Entidad Principal

CommitmentReliabilityScore

## Atributos

- employee_id
- week_id
- score
- trend
- calculated_at

---

# Casos de Uso

- CalculateCRSUseCase
- RecalculateCRSUseCase
- GenerateTeamCRSUseCase
- GenerateProjectCRSUseCase
- GeneratePhaseCRSUseCase

---

# Reportes

- CRS Individual
- CRS Equipo
- CRS Proyecto
- CRS Fase

---

# Reglas

- CRS siempre deriva de Check-In y Check-Out.
- No puede modificarse manualmente.
- Debe ser auditable.

---

# Evolución Futura

- Predicción de riesgo.
- Team Reliability Index.
- Benchmarks organizacionales.
