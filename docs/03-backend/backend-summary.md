# Backend Summary

## Arquitectura Seleccionada

Modular Monolith
+
Clean Architecture por Módulo
+
DDD Lite

## Stack

- FastAPI
- PostgreSQL
- Redis
- Docker Compose

## Módulos

- Auth
- Users
- Teams
- Projects
- Priorities
- CheckIn
- CheckOut
- CRS
- Reporting
- AI Insights

## Jerarquía del Dominio

Proyecto
  ↓
Fase Proyecto
  ↓
Prioridad
  ↓
Tarea

## Principales Beneficios

- Mantenibilidad
- Escalabilidad progresiva
- Bajo acoplamiento
- Alta testabilidad

## Evolución

Docker Compose
  ↓
Kubernetes
  ↓
Extracción selectiva de servicios
