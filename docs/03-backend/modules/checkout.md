
# Check-Out Module

## Objetivo

Gestionar el cierre semanal de compromisos.

---

# Responsabilidades

- Registrar resultados.
- Registrar bloqueadores.
- Marcar prioridades completadas.
- Marcar tareas completadas.
- Definir continuidad.

---

# Flujo Principal

Empleado
    ↓
Revisa Prioridades
    ↓
Marca Completadas
    ↓
Registra Bloqueadores
    ↓
Define Continuidad
    ↓
Check-Out Completado

---

# Entidad Principal

WeeklyCheckOut

## Atributos

- id
- employee_id
- week_id
- comments
- blockers
- completed_at

---

# Casos de Uso

- CreateWeeklyCheckOutUseCase
- CompletePriorityUseCase
- CompleteTaskUseCase
- RegisterBlockersUseCase
- CloseWeekUseCase

---

# Reglas de Negocio

- Un Check-Out por semana.
- No puede existir Check-Out sin Check-In.
- El empleado puede continuar prioridades.
- Las tareas completadas no se duplican.

---

# Dependencias

CheckIn
Priorities
CRS
