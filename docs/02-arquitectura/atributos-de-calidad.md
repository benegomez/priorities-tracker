# Atributos de Calidad

## Objetivo

Definir los atributos de calidad que guiarán la evolución arquitectónica del producto.

---

# Mantenibilidad

Prioridad: Alta

## Justificación

El producto evolucionará rápidamente durante los primeros años.

## Objetivos

- Código modular.
- Baja complejidad.
- Fácil onboarding.

## Métricas

- Cobertura mínima: 70%
- Tiempo onboarding < 2 semanas

---

# Seguridad

Prioridad: Alta

## Objetivos

- Protección de datos organizacionales.
- Protección de cuentas.

## Requerimientos

- JWT
- RBAC
- Password hashing
- HTTPS

## Métricas

- 100% endpoints autenticados
- 0 credenciales en código fuente

---

# Observabilidad

Prioridad: Alta

## MVP

- Logging estructurado JSON
- Correlation IDs

## Futuro

- OpenTelemetry
- Trazabilidad distribuida
- Métricas

## Métricas

- 100% errores registrados

---

# Disponibilidad

Prioridad: Media

## Objetivo

Disponibilidad mínima del servicio.

## Meta

99% uptime durante MVP

---

# Escalabilidad

Prioridad: Media

## Objetivo

Soportar crecimiento progresivo.

## Estrategia

1. Escalado vertical.
2. Kubernetes.
3. Separación selectiva.

---

# Rendimiento

Prioridad: Media

## Objetivos

API REST:

- P95 < 500ms

Base de Datos:

- Consultas críticas < 200ms

---

# Testabilidad

Prioridad: Alta

## Objetivos

- Unit Tests.
- Integration Tests.
- API Tests.

## Beneficios

- Menor regresión.
- Mayor confianza en despliegues.

---

# Escenarios de Calidad

## Escenario 1

Cuando un empleado realiza un Check-In:

El sistema debe responder en menos de 2 segundos.

## Escenario 2

Cuando falle un proveedor IA:

El sistema debe continuar operando sin afectar funcionalidades principales.

## Escenario 3

Cuando exista crecimiento de usuarios:

La aplicación debe poder migrarse a Kubernetes sin reescritura significativa.
