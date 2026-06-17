
# Check-In Module

## Objetivo

Gestionar el proceso de planificación semanal de los colaboradores.

El Check-In es el mecanismo mediante el cual un empleado declara sus compromisos para la semana.

---

# Responsabilidades

- Registrar compromisos semanales.
- Seleccionar proyectos.
- Seleccionar fases de proyecto.
- Crear prioridades.
- Crear tareas.
- Continuar prioridades de semanas anteriores.
- Registrar riesgos iniciales.

---

# Flujo Principal

Empleado
    ↓
Selecciona Proyecto
    ↓
Selecciona Fase
    ↓
Define Prioridades
    ↓
Define Tareas
    ↓
Registra Riesgos
    ↓
Check-In Completado

---

# Entidad Principal

WeeklyCheckIn

## Atributos

- id
- employee_id
- week_id
- status
- comments
- created_at

---

# Casos de Uso

- CreateWeeklyCheckInUseCase
- AddPriorityToCheckInUseCase
- AddTaskToPriorityUseCase
- ContinuePriorityUseCase
- CompleteCheckInUseCase

---

# Reglas de Negocio

- Sólo un Check-In por semana.
- Toda prioridad requiere proyecto y fase.
- El empleado puede continuar prioridades anteriores.
- El Check-In puede permanecer en Draft.

---

# Dependencias

Projects
Priorities
Users
