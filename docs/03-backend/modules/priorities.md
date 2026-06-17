# Priorities Module

## Objetivo

Gestionar compromisos semanales y trabajo ejecutable.

## Ownership

- Priority
- Task

## Relación de Dominio

Project
    ↓
ProjectPhase
    ↓
Priority
    ↓
Task

## Responsabilidades

- Crear prioridades.
- Gestionar tareas.
- Seguimiento semanal.
- Continuidad entre semanas.
- Preparar información para CRS.

## Entidades

### Priority

Compromiso semanal definido por el colaborador.

Campos:

- id
- phase_id
- title
- description
- status

### Task

Unidad mínima de trabajo.

Campos:

- id
- priority_id
- title
- status

## Ciclo de Vida de Prioridad

Draft -> Planned -> In Progress -> Completed -> Carried Over

## Ciclo de Vida de Tarea

Pending -> In Progress -> Completed -> Cancelled

## Casos de Uso

- CreatePriorityUseCase
- UpdatePriorityUseCase
- CarryOverPriorityUseCase
- CreateTaskUseCase
- CompleteTaskUseCase

## Reglas de Negocio

- Toda prioridad pertenece a una fase.
- Toda tarea pertenece a una prioridad.
- Una prioridad puede continuar a otra semana.
- Las tareas completadas no se copian automáticamente.

## Relación con Check-In

Durante Check-In:

1. Seleccionar proyecto.
2. Seleccionar fase.
3. Crear prioridad.
4. Crear tareas.

## Relación con Check-Out

Durante Check-Out:

- Marcar prioridades completadas.
- Marcar tareas completadas.
- Seleccionar elementos a continuar.

## Relación con CRS

El módulo CRS utiliza:

- Prioridades comprometidas.
- Prioridades completadas.
- Tareas comprometidas.
- Tareas completadas.
- Arrastres.

## Métricas

- Prioridades creadas.
- Prioridades completadas.
- Tareas completadas.
- Tasa de arrastre.

## Invariantes

- No existen tareas sin prioridad.
- No existen prioridades sin fase.
- No existen prioridades sin proyecto indirecto.
