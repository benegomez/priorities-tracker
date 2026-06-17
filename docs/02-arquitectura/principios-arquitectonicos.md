# Principios Arquitectónicos

## Objetivo

Este documento define los principios que deben guiar todas las decisiones técnicas de Priorities Tracker.

---

## Principio 1: La lógica de negocio pertenece al dominio

Toda regla de negocio debe implementarse en la capa de dominio.

### Correcto
- Cálculo del CRS.
- Validación de Check-In.
- Reglas de continuidad de prioridades.

### Incorrecto
- Lógica en controladores.
- Lógica en repositorios.
- Lógica en componentes UI.

---

## Principio 2: Arquitectura orientada al dominio

Los módulos deben organizarse alrededor del negocio:

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

No deben organizarse por tecnología.

---

## Principio 3: Bajo acoplamiento

Los módulos sólo deben comunicarse mediante contratos definidos.

Beneficios:
- Mantenibilidad.
- Testabilidad.
- Evolución futura.

---

## Principio 4: Integraciones desacopladas

Toda integración externa debe utilizar adaptadores.

Ejemplos:
- PostgreSQL
- Redis
- OpenAI
- Anthropic

---

## Principio 5: AI Gateway obligatorio

Ningún módulo puede invocar directamente un proveedor LLM.

Siempre:

Modulo -> AI Gateway -> Proveedor IA

Beneficios:
- Cambio de proveedor.
- Control de costos.
- Observabilidad.

---

## Principio 6: Observabilidad desde el diseño

Toda funcionalidad crítica debe generar:

- Logs estructurados.
- Correlation IDs.
- Eventos de auditoría.

---

## Principio 7: Seguridad por defecto

Todo endpoint debe asumir acceso denegado por defecto.

Controles:
- JWT.
- RBAC.
- Auditoría.

---

## Principio 8: Evolución progresiva

La arquitectura debe permitir:

Docker Compose -> Kubernetes -> Extracción Selectiva de Servicios

Sin rediseño completo.
