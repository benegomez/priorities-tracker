# Aggregate Diagrams

## Organization Aggregate

Organization
├─ Teams
├─ Users
├─ Projects
└─ CRS Records

Aggregate Root: Organization

---

## Project Aggregate

Project
└─ ProjectPhase

Aggregate Root: Project

Reglas:
- Una fase no existe sin proyecto.
- Una fase pertenece a un único proyecto.

---

## Priority Aggregate

Priority
└─ Task

Aggregate Root: Priority

Reglas:
- Una tarea no existe sin prioridad.
- Toda prioridad pertenece a una fase.
