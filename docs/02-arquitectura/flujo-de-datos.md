# Flujo de Datos

## Objetivo

Documentar los principales flujos funcionales de Priorities Tracker.

---

# Flujo de Check-In

## Descripción

El empleado registra los compromisos de la semana.

```mermaid
flowchart LR

empleado["Empleado"]

frontend["Frontend"]

api["FastAPI"]

checkin["Check-In Module"]

priorities["Priority Module"]

db["PostgreSQL"]

empleado --> frontend

frontend --> api

api --> checkin

checkin --> priorities

priorities --> db
```

## Resultado

- Prioridades registradas.
- Tareas registradas.
- Riesgos iniciales registrados.

---

# Flujo de Check-Out

## Descripción

El empleado registra resultados obtenidos.

```mermaid
flowchart LR

empleado["Empleado"]

checkout["Check-Out"]

crs["CRS Engine"]

reports["Reporting"]

db["PostgreSQL"]

empleado --> checkout

checkout --> crs

crs --> reports

reports --> db
```

## Resultado

- Cumplimiento calculado.
- Actualización CRS.
- Tendencias actualizadas.

---

# Flujo CRS

## Descripción

Generación del Commitment Reliability Score.

```mermaid
flowchart LR

checkin["Check-In"]

checkout["Check-Out"]

crs["CRS Engine"]

score["CRS Score"]

checkin --> crs

checkout --> crs

crs --> score
```

## Factores Considerados

- Prioridades completadas.
- Tareas completadas.
- Arrastres.
- Consistencia histórica.

---

# Flujo IA

## Descripción

Generación de insights para managers.

```mermaid
flowchart LR

manager["Manager"]

reports["Reporting"]

ai["AI Insights"]

gateway["AI Gateway"]

llm["Proveedor LLM"]

manager --> reports

reports --> ai

ai --> gateway

gateway --> llm

llm --> gateway

gateway --> ai
```

## Resultado

- Resúmenes automáticos.
- Riesgos.
- Recomendaciones.

---

# Flujo de Notificaciones

```mermaid
flowchart LR

scheduler["Scheduler"]

notify["Notification Module"]

user["Usuario"]

scheduler --> notify

notify --> user
```

## Casos de Uso

- Recordatorio Check-In.
- Recordatorio Check-Out.
- Alertas futuras.

---

# Consideraciones de Observabilidad

Todos los flujos deben registrar:

- Correlation ID.
- Logs estructurados.
- Errores.
- Métricas futuras.

---

# Evolución Futura

Incorporar:

- Event Queue.
- Procesamiento asíncrono.
- OpenTelemetry.
- Métricas de negocio.
