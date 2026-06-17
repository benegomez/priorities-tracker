# Visión General de Arquitectura

## Introducción

Priorities Tracker es una plataforma SaaS orientada al seguimiento de prioridades y compromisos semanales.
Su arquitectura debe favorecer la velocidad de entrega, simplicidad operativa y capacidad de evolución.

## Drivers Arquitectónicos

### Drivers de Negocio

- Seguimiento de prioridades.
- Medición de cumplimiento.
- Commitment Reliability Score (CRS).
- Equipos pequeños y medianos.
- Reducción de reuniones de seguimiento.

### Drivers Técnicos

- Time-to-market rápido.
- Costos operativos bajos.
- Alta mantenibilidad.
- Escalabilidad progresiva.
- Integración con IA.

## Arquitectura Seleccionada

### Modular Monolith

La aplicación se implementará como un monolito modular con límites claros entre dominios.

Módulos principales:

- Auth
- Users
- Teams
- Projects
- Priorities
- Check-In
- Check-Out
- CRS
- Reporting
- AI Insights

### Clean Architecture

Capas:

- API Layer
- Application Layer
- Domain Layer
- Infrastructure Layer

## Comparación con Microservicios

### Ventajas del Monolito Modular

- Menor complejidad.
- Menor costo.
- Despliegue simple.
- Observabilidad sencilla.

### Desventajas

- Escalado menos granular.
- Un único despliegue.

## Estrategia de Evolución

Fase 1:
Docker Compose

Fase 2:
Kubernetes

Fase 3:
Extracción selectiva de servicios críticos.

## Beneficios

- Simplicidad operacional.
- Menor deuda técnica inicial.
- Facilidad de onboarding.

## Riesgos

- Crecimiento excesivo del monolito.
- Acoplamiento entre módulos.
- Complejidad creciente del CRS.

## Trade-offs

| Beneficio | Sacrificio |
|------------|------------|
| Simplicidad | Menor independencia |
| Menor costo | Menor granularidad |
| Rapidez | Disciplina arquitectónica |
