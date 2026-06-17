# Projects Module

## Objetivo

Administrar la estructura de planificación de alto nivel del negocio mediante Proyectos y Fases de Proyecto.

## Ownership del Dominio

Este módulo es propietario exclusivo de:

- Project
- ProjectPhase

## Jerarquía Oficial

Proyecto
    ↓
Fase Proyecto
    ↓
Prioridad
    ↓
Tarea

## Responsabilidades

- Crear proyectos.
- Gestionar fases.
- Definir estados.
- Controlar ciclo de vida.
- Exponer información para Priorities.

## Entidades

### Project

Representa una iniciativa organizacional.

Atributos principales:

- id
- name
- description
- owner_id
- status

### ProjectPhase

Representa una etapa específica de ejecución.

Ejemplos:

- Planeación
- Diseño
- Desarrollo
- Implementación
- Capacitación

## Ciclo de Vida del Proyecto

Draft -> Active -> On Hold -> Completed -> Archived

## Ciclo de Vida de la Fase

Planned -> Active -> Completed -> Cancelled

## Casos de Uso

- CreateProjectUseCase
- UpdateProjectUseCase
- CreateProjectPhaseUseCase
- UpdateProjectPhaseUseCase
- CloseProjectUseCase

## Reglas de Negocio

- Toda fase pertenece a un proyecto.
- Un proyecto debe tener al menos una fase activa para recibir prioridades.
- No se pueden registrar prioridades sobre proyectos archivados.

## Invariantes

- project_id obligatorio en ProjectPhase.
- No existen fases huérfanas.
- Una prioridad siempre referencia una fase válida.

## Dependencias

Projects -> Priorities

## Evolución Futura

- Dependencias entre fases.
- Roadmaps.
- Métricas por fase.
