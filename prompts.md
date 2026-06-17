> Detalla en esta sección los prompts principales utilizados durante la creación del proyecto, que justifiquen el uso de asistentes de código en todas las fases del ciclo de vida del desarrollo. Esperamos un máximo de 3 por sección, principalmente los de creación inicial o  los de corrección o adición de funcionalidades que consideres más relevantes.
Puedes añadir adicionalmente la conversación completa como link o archivo adjunto si así lo consideras


## Índice

1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Modelo de datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de usuario](#5-historias-de-usuario)
6. [Tickets de trabajo](#6-tickets-de-trabajo)
7. [Pull requests](#7-pull-requests)

---

## 1. Descripción general del producto

**Prompt 1:**

Revisa el sieguiente prompot, y modificalo para crear un prompt eficiente, y que pueda cumplir con lo que estamos buscando, para buscar mayor claridad. Si necesitas aclarar algun punto, puedes preguntar antes de iniciar "Actua como product manager, experto en sistemas de administración de tareas. Queremos crear una nueva aplicacion web que permita a Managers, llevar un control de las prioridades de sus subordinados y como van avanzando. La idea es que los empleados puedan realizar su check-in de actividades de una forma muy facil y rapida. Adicionalmente esto permitira al manager puder ver cuales son las prioridades y como van cumpliendo metas semana a semana.  El administrador podra dar de alta proyectos sobre los cuales los empleados van a registrar sus Prioridades de la semana. Un empleado al inicio de semana debera realizar su checkin, seleccionando en que proyectos van a trabajar, y podran dar de alta algunas prioridades y en cada prioridad prodran dar de alta tareas especificas.  Al final de la semana el emplado tendra que realizar su checkout, marcando cuales de sus actividades se cumplerieron, agregar notas, y tambien pueden marcar cuales de esas tareas se tendran que continuar en la siguiente semana. El empleado en la siguiente semana al hacer checkin, tendra disponible las mismas prioridades de la semana pasada y podra marcar cuales continuara la semana en curso, ya sea las tareas que marco como que continuara, y poder agregar tareas adicionales. Para el manager debera tener vistas para revisar checkin, checkouts de cada empleados, asi como reportes de desempeño. Se debera considerar un agente de IA para poder generar reportes, medir desempeño, generar KPI, etc.  Busquemos algun feature diferenciador contra sistemas similares al que estamos describiendo, competencia "TEAMSPACE"

**Prompt 2:**
Actúa como un Product Manager Senior especializado en SaaS B2B, gestión de desempeño, productividad y seguimiento de equipos.

Ayúdame a definir estratégicamente una nueva aplicación web enfocada en managers de equipos pequeños (5 a 50 personas) que necesitan visibilidad sobre las prioridades, compromisos y avances de sus colaboradores.

Visión General del Producto

La aplicación NO es un gestor de proyectos tradicional.

Su propósito principal es:

* Dar seguimiento a las prioridades semanales de los empleados.
* Medir cumplimiento de compromisos.
* Facilitar conversaciones de seguimiento entre managers y colaboradores.
* Generar visibilidad del avance real de los proyectos.
* Reducir la necesidad de reuniones de status largas.
* Identificar riesgos y retrasos de forma temprana.

La filosofía central del producto es:

“Los empleados dedican menos de 5 minutos por semana a actualizar sus compromisos y los managers obtienen una visión clara de prioridades, cumplimiento y desempeño.”

Contexto de Negocio

La aplicación estará orientada principalmente a equipos pequeños y medianos donde los managers necesitan conocer:

* Qué se comprometió a realizar cada colaborador.
* Qué logró completar.
* Qué quedó pendiente.
* Qué riesgos o bloqueadores existen.
* Cómo evoluciona el cumplimiento de compromisos a lo largo del tiempo.

El objetivo NO es administrar proyectos complejos.

El objetivo es administrar compromisos y prioridades semanales.

Roles del Sistema

Administrador

Responsable de:

* Crear proyectos.
* Crear fases dentro de los proyectos.
* Crear equipos.
* Gestionar usuarios.
* Asignar managers.
* Configurar ciclos semanales.

Manager

Responsable de:

* Revisar prioridades activas de sus colaboradores.
* Visualizar check-ins semanales.
* Visualizar check-outs semanales.
* Dar seguimiento a compromisos.
* Identificar riesgos.
* Detectar retrasos.
* Facilitar reuniones de seguimiento.
* Evaluar tendencias de cumplimiento.

Empleado

Al inicio de cada semana realiza un Check-In:

1. Selecciona los proyectos donde trabajará.
2. Selecciona la fase correspondiente del proyecto.
3. Define prioridades para la semana.
4. Registra tareas específicas para cada prioridad.
5. Decide qué prioridades pendientes de la semana anterior continuará.
6. Registra riesgos o comentarios.

Jerarquía funcional:

Proyecto → Fase → Prioridad → Tarea

Durante la semana:

* Actualiza avances.
* Registra bloqueadores.
* Agrega comentarios.

Al finalizar la semana realiza un Check-Out:

* Marca prioridades completadas.
* Marca tareas completadas.
* Registra comentarios finales.
* Identifica bloqueadores encontrados.
* Define qué tareas y prioridades continuarán la siguiente semana.

Diferenciador Estratégico Principal

El principal diferenciador debe ser un sistema de medición de cumplimiento llamado:

Commitment Reliability Score (CRS)

El CRS mide qué tan consistentemente una persona cumple los compromisos que ella misma definió.

Ejemplos de indicadores considerados:

* Prioridades comprometidas vs completadas.
* Tareas comprometidas vs completadas.
* Frecuencia de arrastre de prioridades a semanas futuras.
* Consistencia de cumplimiento durante varias semanas.
* Tendencia de mejora o deterioro.

El objetivo es ayudar a managers a entender:

* Quién cumple consistentemente.
* Quién se sobrecompromete.
* Quién requiere apoyo.
* Quién presenta riesgos recurrentes.
* Cómo evoluciona la confiabilidad del equipo en el tiempo.

Este concepto debe considerarse uno de los pilares fundamentales de la propuesta de valor del producto.

Inteligencia Artificial

La IA es una funcionalidad complementaria.

Debe actuar como un asistente para managers.

Ejemplos:

* Resumir check-ins.
* Resumir check-outs.
* Detectar riesgos.
* Identificar prioridades estancadas.
* Identificar posibles sobrecargas.
* Generar insights automáticos.
* Preparar información para reuniones de seguimiento.

La IA no debe reemplazar la gestión humana ni ser el principal diferenciador del producto.

Investigación Esperada

Al generar la respuesta, analiza herramientas similares del mercado (incluyendo Teamspace y otras plataformas de seguimiento de equipos) para identificar oportunidades de diferenciación.

Entregables Solicitados

Limita la respuesta exclusivamente a los siguientes entregables:

1. Product Vision.
2. Value Proposition.
3. User Personas.
4. User Stories.
5. Casos de Uso.

Para cada entregable:

* Profundiza en el análisis.
* Explica el razonamiento detrás de cada decisión.
* Identifica riesgos y supuestos.
* Incluye recomendaciones de producto.
* Mantén una visión orientada a SaaS B2B para equipos pequeños.
* Evita entrar en arquitectura técnica, modelo de datos o diseño de interfaces, ya que esos temas se abordarán en etapas posteriores.


**Prompt 3:**

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**

**Prompt 1:**
Actúa como un Software Architect Senior especializado en SaaS B2B, arquitectura cloud-native y sistemas distribuidos.

Estoy diseñando una aplicación llamada Priorities Tracker.

Contexto del Producto

Priorities Tracker es una plataforma SaaS para seguimiento de prioridades y compromisos semanales.

Los colaboradores realizan:

* Check-In semanal.
* Registro de prioridades.
* Registro de tareas.
* Actualización de avances.
* Check-Out semanal.

Los managers pueden:

* Consultar prioridades activas.
* Revisar cumplimiento.
* Detectar riesgos.
* Revisar métricas de desempeño.
* Consultar el Commitment Reliability Score (CRS).

El sistema incluye funcionalidades de IA para:

* Resumen de check-ins.
* Resumen de check-outs.
* Generación de insights.
* Preparación de reuniones 1:1.
* Detección de riesgos.

Stack Tecnológico Obligatorio

Frontend:

* React
* Next.js

Backend:

* Python
* FastAPI

Persistencia:

* PostgreSQL
* Redis

Contenedores:

* Docker
* Docker Compose

Observabilidad:

* Logging estructurado desde el MVP
* OpenTelemetry considerado para futuras versiones

Objetivo

Diseñar la arquitectura lógica de la aplicación para el MVP.

Entregables

1. Arquitectura General

Explica:

* Estilo arquitectónico recomendado.
* Patrones utilizados.
* Modular Monolith vs Microservices.
* Justificación de la elección.
* Beneficios.
* Riesgos.
* Trade-offs.

2. C4 - Nivel 1

Generar System Context Diagram.

Incluir:

* Administrador
* Manager
* Empleado
* Servicios IA
* Sistema Priorities Tracker

Usar Mermaid o PlantUML.

3. C4 - Nivel 2

Generar Container Diagram.

Incluir:

* Frontend Next.js
* Backend FastAPI
* PostgreSQL
* Redis
* AI Service
* Sistema de logging

Mostrar relaciones.

Usar Mermaid o PlantUML.

4. C4 - Nivel 3

Generar Component Diagram del Backend.

Incluir:

* Auth Module
* User Module
* Team Module
* Project Module
* Check-In Module
* Check-Out Module
* Priority Module
* CRS Engine
* Reporting Module
* AI Insights Module
* Notification Module

Explicar responsabilidades y relaciones.

5. Decisiones Arquitectónicas

Generar tabla ADR con:

* Decisión
* Alternativas
* Justificación
* Beneficios
* Riesgos

6. Conclusión

Responder:

* ¿Por qué esta arquitectura es adecuada para Priorities Tracker?
* ¿Qué beneficios aporta?
* ¿Qué sacrificios implica?

**Prompt 2:**
Actúa como un Software Architect Senior especializado en Python, FastAPI, IA aplicada a SaaS B2B y arquitecturas mantenibles.

Contexto

La arquitectura general de Priorities Tracker ya fue definida.

Stack:

* FastAPI
* PostgreSQL
* Redis
* Docker Compose

Objetivo

Diseñar la arquitectura interna del backend.

Entregables

1. Arquitectura Backend

Definir:

* Clean Architecture
* Hexagonal Architecture
* DDD Lite
* Modular Monolith

Indicar cuál recomiendas y por qué.

2. C4 Nivel 4

Generar diagrama detallado de módulos.

Mostrar:

* API Layer
* Application Layer
* Domain Layer
* Infrastructure Layer

Mostrar dependencias permitidas.

Usar Mermaid o PlantUML.

3. Organización del Código

Proponer estructura completa de carpetas.

Ejemplo:

backend/
├── app/
├── domain/
├── application/
├── infrastructure/
├── interfaces/
├── tests/

Explicar responsabilidades.

4. Diseño del CRS Engine

Explicar:

* Responsabilidades.
* Entradas.
* Salidas.
* Cómo calcular el Commitment Reliability Score.
* Cómo mantener historial.

5. Diseño del AI Module

Diseñar el módulo de IA.

Incluir:

* Resumen de Check-In.
* Resumen de Check-Out.
* Generación de Insights.
* Detección de Riesgos.
* Preparación de 1:1.

Explicar:

* Flujo de datos.
* Integración con LLMs.
* Prompt orchestration.
* Costos.
* Escalabilidad.

6. Redis

Explicar uso recomendado.

Evaluar:

* Cache
* Rate limiting
* Session storage
* Job queue

7. Observabilidad

Diseñar estrategia MVP.

Incluir:

* Structured Logging
* Correlation IDs
* Error Tracking

Proponer evolución futura:

* OpenTelemetry
* Distributed Tracing
* Metrics

8. Testing Strategy

Definir:

* Unit Testing
* Integration Testing
* API Testing
* End-to-End Testing

9. Riesgos Técnicos

Identificar riesgos futuros y mitigaciones.

**Prompt 3:**

Actúa como un Cloud Architect Senior especializado en Docker, DevOps, despliegues SaaS y plataformas cloud-native.

Contexto

Priorities Tracker utiliza:

Frontend:

* Next.js

Backend:

* FastAPI

Base de datos:

* PostgreSQL

Cache:

* Redis

IA:

* Servicio dedicado de IA

Contenedores:

* Docker Compose

Objetivo

Diseñar la arquitectura de infraestructura y despliegue.

Entregables

1. Arquitectura de Despliegue

Generar Deployment Diagram.

Mostrar:

* Docker Compose
* Frontend Container
* Backend Container
* PostgreSQL Container
* Redis Container
* AI Service Container

Mostrar redes y relaciones.

Usar Mermaid o PlantUML.

2. Docker Compose Design

Explicar:

* Servicios.
* Redes.
* Volúmenes.
* Variables de entorno.

Justificar diseño.

3. Seguridad

Diseñar:

* JWT Authentication
* RBAC
* Secret Management
* API Security
* Password Policies
* Audit Logs

Explicar beneficios y riesgos.

4. Logging

Diseñar:

* Centralización de logs.
* Formato estructurado.
* Retención.
* Búsqueda.

Proponer herramientas.

5. Escalabilidad

Explicar:

* Escalamiento vertical.
* Escalamiento horizontal.
* Cuellos de botella esperados.

6. Migración a Kubernetes

Explicar:

* Qué componentes migrarían primero.
* Cambios requeridos.
* Beneficios.
* Costos.

7. Alta Disponibilidad

Analizar:

* PostgreSQL
* Redis
* Backend
* Frontend

Indicar qué mecanismos aplicarías cuando el producto crezca.

8. Costos Operativos

Proponer:

* Arquitectura MVP de bajo costo.
* Arquitectura para 100 usuarios.
* Arquitectura para 1,000 usuarios.
* Arquitectura para 10,000 usuarios.

9. Conclusión

Responder:

* ¿Por qué Docker Compose es la mejor opción para el MVP?
* ¿Cuándo debería migrarse a Kubernetes?
* ¿Qué limitaciones tendrá la arquitectura inicial?

### **2.2. Descripción de componentes principales:**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.4. Infraestructura y despliegue**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.5. Seguridad**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.6. Tests**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 3. Modelo de Datos

**Prompt 1:**
Actúa como un Database Architect Senior especializado en PostgreSQL, SaaS B2B multi-tenant y sistemas de gestión de desempeño.

Estoy diseñando una aplicación llamada Priorities Tracker.

Contexto del Producto

Priorities Tracker es una plataforma SaaS para seguimiento de prioridades semanales, compromisos, desempeño y confiabilidad de cumplimiento.

La jerarquía oficial del dominio es:

Proyecto
    ↓
Fase Proyecto
    ↓
Prioridad
    ↓
Tarea

El sistema incluye:

- Check-In semanal
- Check-Out semanal
- Reporting
- Commitment Reliability Score (CRS)
- AI Insights

Stack Tecnológico

Backend:
- Python
- FastAPI

Persistencia:
- PostgreSQL
- Redis

Deployment:
- Docker Compose

Arquitectura ya aprobada:

- Modular Monolith
- Clean Architecture por módulo
- Multi-tenant SaaS

Decisiones de Dominio Aprobadas

Aggregate Root principal:

Organization

Todos los datos pertenecen a una organización.

Estrategia Multi-Tenant:

Shared Database
Shared Schema
Tenant Column

Tenant Key:

organization_id

Entidades principales:

Organization
Team
User

Project
ProjectPhase

Priority
Task

WeeklyCheckIn
WeeklyCheckOut

CommitmentReliabilityScore

Objetivo

Diseñar la arquitectura completa de persistencia PostgreSQL para el MVP.

Entregables

1. Database Overview

Explicar:

- Objetivos de la persistencia
- Estrategia PostgreSQL
- Justificación técnica

2. ER Model

Generar:

- Modelo Entidad Relación
- Cardinalidades
- Ownership de agregados

Usar Mermaid compatible GitHub.

3. Logical Model

Definir:

- Entidades
- Relaciones
- Dependencias

4. Physical Model

Definir:

- Tablas
- Tipos PostgreSQL
- UUID Strategy
- Naming Convention

5. Table Definitions

Para cada tabla definir:

- Columnas
- Tipo
- Nullable
- Default
- Descripción

6. Index Strategy

Definir:

- Índices simples
- Índices compuestos
- Índices para reporting
- Índices para CRS

7. Constraints

Definir:

- PK
- FK
- Unique Constraints
- Check Constraints

8. Audit Strategy

Definir:

- created_at
- updated_at
- created_by
- updated_by
- soft delete

9. Multi-Tenant Strategy

Explicar:

- Tenant Isolation
- Query Filtering
- Seguridad

10. Migration Strategy

Definir:

- Alembic
- Versionado
- Convenciones

11. Performance Strategy

Definir:

- Caching Redis
- Reporting
- CRS
- Escalabilidad futura

12. Conclusión

Responder:

- ¿Por qué este diseño soporta Priorities Tracker?
- ¿Qué beneficios aporta?
- ¿Qué riesgos o trade-offs implica?

Generar documentación profesional orientada a PostgreSQL y SaaS B2B.
**Prompt 2:**

**Prompt 3:**

---

### 4. Especificación de la API

**Prompt 1:**

Actúa como un Software Architect Senior especializado en FastAPI, Clean Architecture, DDD Lite y SaaS B2B.

Estoy desarrollando una aplicación llamada Priorities Tracker.

Contexto

Priorities Tracker ya cuenta con:

- Arquitectura aprobada
- Modelo de dominio aprobado
- Diseño PostgreSQL aprobado

Stack Tecnológico

Frontend:
- React
- Next.js

Backend:
- Python
- FastAPI

Persistencia:
- PostgreSQL
- Redis

Contenedores:
- Docker Compose

Arquitectura Backend

- Modular Monolith
- Clean Architecture por módulo

Módulos aprobados:

Auth
Users
Teams
Projects
Priorities
CheckIn
CheckOut
CRS
Reporting
AI Insights

Jerarquía de Dominio

Proyecto
    ↓
Fase Proyecto
    ↓
Prioridad
    ↓
Tarea

Objetivo

Diseñar la implementación backend completa para el MVP.

Entregables

1. Backend Project Structure

Generar:

src/
├── modules/
├── shared/
├── tests/

Explicar cada carpeta.

2. Module Design

Para cada módulo definir:

- Responsabilidades
- Casos de uso
- Dependencias
- Interfaces

3. FastAPI Router Design

Definir endpoints para:

Auth
Users
Teams
Projects
Project Phases
Priorities
Tasks
CheckIns
CheckOuts
CRS
Reports

Para cada endpoint incluir:

- Método HTTP
- Ruta
- Descripción
- Request
- Response

4. Pydantic Schemas

Definir:

- Request Schemas
- Response Schemas
- Validation Rules

5. SQLAlchemy Models

Definir:

- Modelos por entidad
- Relaciones
- Constraints

6. Repository Pattern

Definir:

- Interfaces
- Implementaciones
- Ejemplos

7. Use Cases

Definir:

Check-In
Check-Out
Priority Management
Task Management
CRS Calculation
Reporting

8. Dependency Injection

Definir:

- FastAPI Dependencies
- Repositories
- Services

9. Async Processing

Definir:

- Redis
- Background Jobs
- CRS Recalculation
- AI Tasks

10. AI Integration

Definir:

- AI Gateway
- Providers
- Prompt Management
- Cost Tracking

11. Security Design

Definir:

- JWT
- RBAC
- Tenant Isolation

12. Testing Strategy

Definir:

- Unit Tests
- Integration Tests
- API Tests
- E2E Tests

13. Implementation Roadmap

Definir:

Orden recomendado de implementación módulo por módulo.

14. Conclusión

Responder:

- ¿Por qué esta implementación es adecuada?
- ¿Qué beneficios aporta?
- ¿Qué riesgos implica?
- ¿Qué partes pueden evolucionar a microservicios en el futuro?

Generar documentación profesional orientada a implementación real en FastAPI.

**Prompt 2:**
Actúa como un Principal Software Architect especializado en Python, FastAPI, SQLAlchemy 2.0, DDD Lite, Clean Architecture y SaaS B2B multi-tenant.

Estoy desarrollando una aplicación llamada Priorities Tracker.

Contexto

Priorities Tracker es una plataforma SaaS para gestión de prioridades semanales, seguimiento de compromisos y medición de desempeño.

La jerarquía oficial del dominio es:

Proyecto
    ↓
Fase Proyecto
    ↓
Prioridad
    ↓
Tarea

El sistema incluye:

- Check-In semanal
- Check-Out semanal
- Commitment Reliability Score (CRS)
- Reporting
- AI Insights

Stack Tecnológico

Backend:
- Python 3.13+
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- Alembic

Persistencia:
- PostgreSQL
- Redis

Arquitectura:

- Modular Monolith
- Clean Architecture por módulo
- Multi-Tenant SaaS

Decisiones Aprobadas

Multi-Tenant:

Shared Database
Shared Schema
Tenant Column

Tenant Key:

organization_id

Aggregate Root superior:

Organization

Jerarquía congelada:

Proyecto
    ↓
Fase Proyecto
    ↓
Prioridad
    ↓
Tarea

Módulos existentes:

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

Objetivo

Diseñar completamente la capa ORM y persistencia utilizando SQLAlchemy 2.0.

La salida debe servir como especificación para que un equipo de desarrollo implemente directamente los modelos y repositorios.

Entregables

1. SQLAlchemy Design Overview

Explicar:

- Filosofía ORM adoptada.
- Relación con Clean Architecture.
- Relación con el dominio.
- Beneficios.
- Riesgos.
- Trade-offs.

2. SQLAlchemy Conventions

Definir:

- Declarative Base
- Naming Conventions
- UUID Strategy
- Timestamp Strategy
- Soft Delete Strategy
- Audit Fields Strategy

Generar ejemplos.

3. Base Entity Design

Diseñar:

BaseEntity

OrganizationScopedEntity

AuditEntity

Explicar:

- Responsabilidades
- Campos comunes
- Herencia

Generar diagramas Mermaid compatibles con GitHub.

4. Entity Mappings

Diseñar modelos SQLAlchemy completos para:

Organization
Team
User

Project
ProjectPhase

Priority
Task

WeeklyCheckIn
WeeklyCheckOut

CommitmentReliabilityScore

Para cada entidad definir:

- Tabla
- Campos
- Tipos
- Constraints
- Índices
- Relaciones

5. Relationship Design

Explicar:

Organization → Teams
Team → Users

Project → Phases
Phase → Priorities
Priority → Tasks

User → CheckIns
User → CheckOuts
User → CRS

Definir:

- One-to-Many
- Many-to-One
- Cascade Rules
- Lazy Loading Strategy

Justificar decisiones.

6. Multi-Tenant Design

Explicar:

- organization_id
- Tenant Isolation
- Query Filtering

Definir:

OrganizationScopedRepository

Generar ejemplos.

7. Repository Pattern

Diseñar:

BaseRepository

OrganizationScopedRepository

ProjectRepository

PriorityRepository

CheckInRepository

CheckOutRepository

CRSRepository

Para cada uno definir:

- Interface
- Responsabilidades
- Métodos

Generar ejemplos de código.

8. Unit of Work Pattern

Diseñar:

UnitOfWork

SQLAlchemyUnitOfWork

Explicar:

- Transaction Boundaries
- Commit
- Rollback

Generar ejemplos.

9. Query Specifications

Diseñar patrones para:

Prioridades activas
Prioridades vencidas
CRS histórico
Dashboard Manager
Dashboard Ejecutivo

Explicar:

- Filtros
- Ordenamientos
- Paginación

10. Transaction Boundaries

Definir:

Check-In Flow
Check-Out Flow
CRS Calculation Flow

Explicar:

- Qué ocurre dentro de una transacción.
- Qué ocurre fuera de la transacción.

11. Performance Considerations

Explicar:

- selectinload
- joinedload
- índices
- N+1 problems
- reporting

12. Testing Strategy

Definir:

- Repository Tests
- Transaction Tests
- Integration Tests

13. ORM Summary

Generar una tabla final que muestre:

Entidad
Tabla
Aggregate
Repository
Owner Module

14. Conclusión

Responder:

- ¿Por qué este diseño ORM es adecuado para Priorities Tracker?
- ¿Qué beneficios aporta?
- ¿Qué riesgos implica?
- ¿Qué recomendaciones existen para una futura migración a microservicios?

Importante:

Mantener consistencia con todas las decisiones tomadas previamente en:

- Arquitectura
- Dominio
- PostgreSQL
- Multi-Tenant
- CRS

La documentación debe tener nivel profesional y servir como blueprint de implementación para SQLAlchemy 2.0.

**Prompt 3:**

---

### 5. Historias de Usuario

**Prompt 1:**

---
description: Selecciona y crea la siguiente User Story de mayor valor para el MVP de Priorities Tracker, usando las personas definidas y el criterio de valor de negocio sobre simplicidad técnica.
---

Por favor selecciona y crea la siguiente user story del MVP: $ARGUMENTS

## Contexto del Proyecto

Lee primero:
- `AmazonQ.md` — módulos, stack, bounded contexts
- `docs/01-product-definition/mvp-definition.md` — scope del MVP
- `docs/01-product-definition/personas.md` — las 3 personas del producto
- `docs/01-product-definition/requirements-functional.md` — FR-001..FR-035
- `docs/01-product-definition/value-proposition.md` — propuesta de valor por persona
- `docs/01-product-definition/success-metrics.md` — métricas del producto
- `.amazonq/rules/domain-standards.md` — bounded contexts y módulos

---

## Parseo de Argumentos

`$ARGUMENTS` puede ser:

| Formato | Comportamiento |
|---|---|
| *(vacío)* | El agente propone y justifica la siguiente historia de mayor valor |
| `<tema o feature>` | Crea una historia sobre ese tema específico (ej. `checkin`, `crs`, `auth`) |
| `list` | Lista las historias candidatas ordenadas por valor, sin crear ninguna |

---

## Paso 1 — Revisar Historias Existentes

- Escanea `docs/user-stories/` para identificar qué historias ya existen.
- Lista las historias ya creadas con su estado (`[original]` only vs. `[enhanced]`).
- Identifica el **gap**: qué capacidades del MVP aún no tienen user story.

---

## Paso 2 — Evaluar Candidatas por Valor

Para cada capacidad sin historia, evalúa su valor usando estos cuatro criterios:

### Criterio 1 — Valor para el Usuario (peso: 40%)

Usa las **3 personas** del producto:

| Persona | Pregunta clave |
|---|---|
| **Manager de Equipo Pequeño** | ¿Le da visibilidad de su equipo en < 5 minutos? ¿Reduce reuniones de status? |
| **Colaborador Individual** | ¿Le permite registrar compromisos en minutos? ¿Reduce interrupciones? |
| **Líder de Área** | ¿Le da visibilidad consolidada sin revisar cada proyecto? |

Puntúa 1-3 según cuántas personas se benefician directamente.

### Criterio 2 — Posición en la Cadena de Valor (peso: 30%)

El MVP tiene una cadena de valor central:

```
Estructura organizacional (users, teams, projects)
        ↓  habilita
Check-In semanal (compromisos)
        ↓  genera
Check-Out semanal (resultados)
        ↓  alimenta
CRS (confiabilidad)
        ↓  visualiza
Dashboards y Reportes (visibilidad)
        ↓  amplifica
AI Insights (inteligencia)
```

Una historia que habilita pasos posteriores de la cadena tiene más valor que una que solo agrega detalle a un paso existente.

Puntúa:
- `3` — Es un paso de la cadena principal sin el que pasos posteriores no funcionan
- `2` — Enriquece un paso existente de la cadena
- `1` — Es complementaria o de soporte

### Criterio 3 — Impacto en Métricas de Éxito (peso: 20%)

Consulta `success-metrics.md`. ¿Esta historia impacta directamente alguna métrica clave?

- North Star: Commitment Completion Rate
- Check-In Completion Rate > 90%
- Check-Out Completion Rate > 85%
- CRS promedio del equipo
- Team Visibility Time < 5 minutos

Puntúa 1-3 según el número de métricas que impacta.

### Criterio 4 — Deuda de Dependencias (peso: 10%)

¿Cuántas otras historias del backlog dependen de esta para poder implementarse?

- `3` — 3 o más historias la necesitan como prerequisito
- `2` — 1-2 historias dependen de ella
- `1` — No tiene dependientes directos

### Scoring Final

```
Score = (Valor usuario × 0.40) + (Cadena de valor × 0.30) + (Métricas × 0.20) + (Dependencias × 0.10)
```

Ordena las candidatas de mayor a menor score. La de mayor score es la siguiente historia a crear.

---

## Paso 3 — Justificar la Selección

Antes de crear la historia, presenta al usuario:

```
Historia seleccionada: <título>
Persona principal: <persona>

Scoring:
  Valor para el usuario:      <score>/3 — <justificación breve>
  Posición en cadena valor:   <score>/3 — <justificación breve>
  Impacto en métricas:        <score>/3 — <justificación breve>
  Deuda de dependencias:      <score>/3 — <justificación breve>
  Score total:                <X.XX>/3

Por qué esta y no otra:
  <2-3 líneas explicando por qué esta historia entrega más valor al producto ahora>

¿Procedemos con esta historia? (sí / elegir otra candidata)
```

Si el usuario responde con otra opción, crear esa historia en su lugar.

---

## Paso 4 — Crear la User Story

Una vez confirmada la historia, crea el archivo en:

```
docs/user-stories/<story-id>/UserStory.md
```

El `story-id` sigue el formato: `<NNN>-<kebab-case-titulo>`
Ejemplo: `001-weekly-checkin-creation`

Estructura del archivo:

```markdown
---
id: <story-id>
persona: <Manager de Equipo Pequeño / Colaborador Individual / Líder de Área>
fr: FR-XXX
bounded-context: <Organization / Commitment / Execution / Reliability>
status: draft
created: <fecha actual>
---

# <Título de la User Story>

## [original]

**Como** <rol específico de la persona>,
**quiero** <acción concreta>,
**para** <beneficio de negocio medible>.

### Contexto
<2-3 líneas describiendo la situación de la persona antes de esta historia — el dolor o necesidad que motiva la historia>

### Notas iniciales
- <observación relevante 1>
- <observación relevante 2>
- <restricción conocida si aplica>
```

---

## Paso 5 — Confirmar

Responde con:

```
✅ User Story creada: docs/user-stories/<story-id>/UserStory.md

Persona:         <nombre de la persona>
FR de referencia: FR-XXX
Bounded Context: <contexto> → Módulo: <módulo>
Score de valor:  <X.XX>/3

Siguiente paso:  /enrich-us <story-id>
```


**Prompt 2:**

---
description: Analiza y enriquece una user story produciendo una especificación lista para implementación siguiendo el flujo Spec-Driven de Priorities Tracker.
---

Por favor analiza y enriquece la user story: $ARGUMENTS

## Contexto del Proyecto

Lee primero:
- `AmazonQ.md` — visión general, módulos, stack
- `.amazonq/rules/base.md` — lenguaje ubicuo y principios
- `.amazonq/rules/domain-standards.md` — entidades, BRs, state machines
- `.amazonq/rules/api-standards.md` — ciclo contract-first
- `docs/01-product-definition/requirements-non-functional.md` — NFR-001..NFR-015
- `docs/01-product-definition/success-metrics.md` — métricas del producto

---

## Paso 1 — Encontrar la User Story

- Busca en `docs/user-stories/` o en la carpeta indicada una historia que coincida con `$ARGUMENTS`.
- Lee el contenido completo del archivo encontrado.
- Si no hay match, lista las historias disponibles y pide clarificación.

---

## Paso 2 — Analizar y Mapear

Identifica y documenta los siguientes elementos antes de escribir el `[enhanced]`:

**Dominio:**
- FR de referencia (FR-001..FR-035)
- Bounded context: Organization / Commitment / Execution / Reliability
- Módulo(s) backend involucrado(s)
- Entidades de dominio afectadas con atributos y validaciones
- Business Rules aplicables (BR-XXX)
- Transiciones de estado involucradas

**Negocio:**
- Usuario principal (rol: administrator / manager / employee)
- Objetivo principal del usuario en esta historia
- Flujo principal de interacción (pasos en orden)
- Problema concreto que resuelve
- Beneficio esperado medible
- Prioridad de negocio: Critical / High / Medium / Low
- NFRs aplicables (NFR-001..NFR-015)
- Métricas de éxito relevantes de `success-metrics.md`
- Dependencias técnicas (otros módulos, tickets) y funcionales (otras US)

**Técnico:**
- Endpoints API necesarios: método, path, descripción
- Contrato API preliminar: request/response shape

---

## Paso 3 — Evaluar Completitud

Una user story lista para implementación debe incluir:
- [ ] User Journey: usuario, objetivo, flujo principal
- [ ] Business Value: problema + beneficio
- [ ] Prioridad de negocio asignada
- [ ] FR de referencia identificado
- [ ] Bounded context y módulo propietario
- [ ] Entidades y campos de datos (inputs, outputs, estado persistido)
- [ ] Business Rules aplicables (BR-XXX)
- [ ] Transiciones de estado (si aplica)
- [ ] Contrato API preliminar (método, path, request/response shape)
- [ ] Criterios de aceptación en Gherkin — mínimo 5
- [ ] NFRs aplicables referenciados
- [ ] Métricas de éxito (1-2 más relevantes)
- [ ] Dependencias identificadas
- [ ] Nivel de riesgo: Low / Medium / High / Critical
- [ ] Complejidad estimada: XS / S / M / L / XL

---

## Paso 3b — Estimar Complejidad

Analiza los siguientes factores y asigna una clasificación:

| Factor | Preguntas a responder |
|---|---|
| **Capas afectadas** | ¿Cuántas capas involucra? (DB, backend, frontend, todas) |
| **Endpoints** | ¿Cuántos endpoints nuevos o modificados? |
| **Entidades** | ¿Cuántas entidades/tablas nuevas o modificadas? |
| **Business Rules** | ¿Cuántas BRs aplican? ¿Alguna es compleja (CRS, carry-over, multi-tenant)? |
| **Integraciones** | ¿Involucra AI, servicios externos, eventos de dominio? |
| **Tests requeridos** | ¿Nivel Critical o High? ¿Requiere E2E? |
| **UI** | ¿Requiere nuevas páginas, flujos complejos, gráficas? |

### Tabla de Clasificación

| Talla | Criterios orientativos | Ejemplo |
|---|---|---|
| **XS** | 1 capa, 1 endpoint simple, sin nueva entidad, sin BRs complejas, sin UI nueva | Cambiar un campo en un response existente |
| **S** | 1-2 capas, 1-2 endpoints, 1 entidad existente modificada, 1-2 BRs simples | Agregar filtro de búsqueda a listado de prioridades |
| **M** | 2-3 capas, 2-4 endpoints, 1 entidad nueva o 2-3 modificadas, hasta 4 BRs, UI moderada | CRUD completo de un recurso con validaciones y pantalla de gestión |
| **L** | 3 capas, 4+ endpoints, 2+ entidades nuevas, BRs complejas o state machine, tests E2E requeridos | Flujo completo de Check-In con prioridades, tareas y validaciones |
| **XL** | 3 capas, flujo end-to-end crítico, múltiples entidades, cálculos complejos (CRS), integraciones externas (AI), cobertura >95% requerida | Cálculo y persistencia del CRS con historial y tendencias |

---

## Paso 4 — Actualizar el Archivo

Sobreescribe el archivo de la user story con la siguiente estructura:

```markdown
# <Título de la User Story>

## [original]

<contenido original intacto — NO modificar>

## [enhanced]

### User Journey
- **Usuario principal:** <rol: administrator / manager / employee>
- **Objetivo principal:** <qué quiere lograr el usuario>
- **Flujo principal:**
  1. <paso 1>
  2. <paso 2>
  3. <paso N>

### Business Value
- **Problema que resuelve:** <descripción concreta del dolor>
- **Beneficio esperado:** <resultado medible para el usuario o el negocio>

### Priority
**<Critical / High / Medium / Low>**
<justificación de 1 línea>

### FR de Referencia
FR-XXX — <descripción>

### Bounded Context
<contexto> → Módulo: <módulo>

### Entidades Involucradas
- `<Entity>`: <atributos relevantes para esta historia>

### Business Rules Aplicables
- **BR-XXX** — <descripción exacta>

### Transiciones de Estado
<si aplica — entidad: Estado A → Estado B>

### Contrato API Preliminar
**<METHOD> /api/v1/<resource>/**
Request:
```json
{ }
```
Response:
```json
{ }
```

### Acceptance Criteria

> Formato Gherkin. Mínimo 5 criterios.

**Escenario 1 — <nombre del escenario happy path>**
```gherkin
Given <contexto inicial>
When <acción del usuario>
Then <resultado esperado>
```

**Escenario 2 — <nombre del escenario de validación>**
```gherkin
Given <contexto inicial>
When <acción inválida>
Then <resultado de error esperado>
```

**Escenario 3 — <nombre del escenario de autorización>**
```gherkin
Given <usuario sin el rol correcto>
When <intenta realizar la acción>
Then <recibe 403 Forbidden>
```

**Escenario 4 — <nombre del escenario de regla de negocio>**
```gherkin
Given <contexto que activa una BR>
When <acción>
Then <sistema aplica la BR correctamente>
```

**Escenario 5 — <nombre del escenario adicional>**
```gherkin
Given <contexto>
When <acción>
Then <resultado>
```

### Non-Functional Requirements
- **NFR-XXX** — <nombre>: <implicación concreta para esta historia>

### Dependencies
- **Técnicas:** <otros módulos, tickets, migraciones previas requeridas>
- **Funcionales:** <otras user stories que deben estar completas primero>

### Success Metrics
- **<KPI del producto>:** <métrica esperada para esta historia>

### Nivel de Riesgo
**<Low / Medium / High / Critical>**

### Complejidad Estimada
**<XS / S / M / L / XL>**

| Factor | Detalle |
|---|---|
| Capas afectadas | <DB / Backend / Frontend / todas> |
| Endpoints | <número y tipo> |
| Entidades | <nuevas / modificadas> |
| Business Rules | <BR-XXX aplicables> |
| Tests requeridos | <nivel y tipos según matriz> |
| Justificación | <razón principal de la talla asignada> |

### Siguiente Paso
Ejecutar `/create-tickets <story-id>`
```

---

## Paso 5 — Confirmar

Responde con:
- Archivo actualizado y su ruta
- Usuario principal y objetivo identificados
- FR mapeado y bounded context
- BRs aplicables
- NFRs referenciados
- Dependencias identificadas
- Nivel de riesgo y complejidad estimada con justificación
- Siguiente paso: `/create-tickets <story-id>`



**Prompt 3:**

---

### 6. Tickets de Trabajo

**Prompt 1:**

---
description: Crea tickets de implementación (database, backend, frontend) a partir de una user story enriquecida de Priorities Tracker.
---

Por favor crea los tickets de implementación de la user story: $ARGUMENTS

## Contexto del Proyecto

Lee primero:
- `AmazonQ.md` — estructura de módulos y stack
- `.amazonq/rules/domain-standards.md` — entidades, BRs, enums
- `.amazonq/rules/api-standards.md` — contrato OpenAPI, schemas Pydantic
- `.amazonq/rules/database-standards.md` — naming, soft delete, audit columns

## Paso 1 — Encontrar la User Story Enriquecida

- Busca el archivo de la user story que coincida con `$ARGUMENTS`.
- Verifica que contenga la sección `## [enhanced]`. Si no existe, detente y pide ejecutar `/enrich-us` primero.

## Paso 2 — Determinar Estrategia de Tests

Antes de crear los tickets, lee de la sección `[enhanced]` de la US:
- **Nivel de riesgo:** Low / Medium / High / Critical
- **Complejidad estimada:** XS / S / M / L / XL

Con esos dos valores, aplica esta matriz para determinar qué tests son obligatorios en cada ticket:

| Nivel de Riesgo | Complejidad | Unit | Integration | Contract | E2E | Security | Cobertura mínima |
|---|---|---|---|---|---|---|---|
| Low | XS / S | ✅ | ❌ | ❌ | ❌ | ❌ | >60% |
| Medium | S / M | ✅ | ✅ | ❌ | ❌ | ❌ | >80% |
| High | M / L | ✅ | ✅ | ✅ | ❌ | ✅ | >80% |
| Critical | L / XL | ✅ | ✅ | ✅ | ✅ | ✅ | >95% |

**Regla adicional por módulo:** independientemente del nivel de riesgo de la US, los módulos `auth`, `checkin`, `checkout` y `crs` siempre requieren nivel Critical.

Guarda mentalmente esta decisión — la usarás para poblar la sección `## Tests Requeridos` de cada ticket.

## Paso 2b — Crear Estructura de Tickets

Dentro de la carpeta de la user story, crea:

```
<story-folder>/
  tickets/
    database/ticket.md
    backend/ticket.md
    frontend/ticket.md
```

## Paso 3 — Ticket Database

> La capa database no tiene tests unitarios propios. Sus criterios de aceptación actúan como tests de verificación manual/migration.

Plantilla para `tickets/database/ticket.md`:

```markdown
---
status: todo
type: database
story: <ruta al UserStory.md>
---

# [DB] <Feature Name>

## Objetivo
<qué persiste esta capa — tablas, columnas, índices>

## Scope
Solo schema PostgreSQL + migraciones Alembic. Sin endpoints, sin lógica de negocio.

## Cambios al Schema

### Tablas nuevas
<nombre_tabla (snake_case plural)>
  - id UUID PK
  - organization_id UUID FK NOT NULL  ← obligatorio en toda entidad
  - <campo> <tipo> <restricciones>
  - created_at TIMESTAMPTZ NOT NULL DEFAULT now()
  - updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
  - deleted_at TIMESTAMPTZ NULL
  - deleted_by UUID NULL

### Columnas nuevas en tablas existentes
<ALTER TABLE ... ADD COLUMN IF NOT EXISTS ...>

### Índices
<CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_<tabla>_<columna>>

## Migración Alembic
Archivo: `apps/backend/src/shared/database/migrations/<YYYYMMDDHHMI>_<descripcion>.py`

## Criterios de Aceptación
- [ ] Tablas/columnas creadas con tipos y restricciones correctas
- [ ] organization_id presente en toda entidad de negocio
- [ ] Columnas de auditoría presentes (created_at, updated_at, deleted_at, deleted_by)
- [ ] Índices creados para todas las FKs
- [ ] Migración ejecuta sin errores
- [ ] downgrade() implementado y probado

## Dependencias
Ninguna. Debe completarse antes del ticket backend.
```

## Paso 4 — Ticket Backend

Plantilla para `tickets/backend/ticket.md`:

```markdown
---
status: todo
type: backend
story: <ruta al UserStory.md>
depends-on: tickets/database/ticket.md
---

# [BE] <Feature Name>

## Objetivo
<lógica de negocio, casos de uso y endpoints a implementar>

## Scope
FastAPI router, Pydantic schemas, casos de uso, repositorios SQLAlchemy. Sin schema SQL, sin UI.

## Dependencia
Ticket database mergeado y migración aplicada.

## FR de Referencia
FR-XXX — <descripción>

## Business Rules Aplicables
- BR-XXX — <descripción>

## Contrato OpenAPI (diseñar ANTES de implementar — ADR-009)

### Endpoint 1
**Método y path:** POST /api/v1/<resource>/
**Tags:** [<módulo>]
**operation_id:** <snake_case_único>
**Auth:** Bearer JWT requerido

Request body:
\`\`\`json
{ }
\`\`\`

Response 201:
\`\`\`json
{ }
\`\`\`

Responses de error: 400, 401, 403, 404, 409

## Archivos a Crear / Modificar

```
apps/backend/src/modules/<module>/
  api/
    router.py          - MODIFY (agregar endpoint)
    schemas.py         - MODIFY (agregar <Entity>Create, <Entity>Response)
    dependencies.py    - MODIFY (si nueva dependency)
  application/
    commands/<action>_command.py    - CREATE
    queries/<query>_query.py        - CREATE (si lectura)
  domain/
    entities/<entity>.py            - CREATE/MODIFY
    repositories/<entity>_repo.py   - MODIFY (agregar método)
  infrastructure/
    repositories/<entity>_repo_impl.py - MODIFY
```

## Casos de Uso a Implementar
- `<ActionNameUseCase>` — descripción

## Validaciones de Dominio
<lista de validaciones que van en dominio/aplicación, NO en el router>

## Tests Requeridos

> Generado automáticamente desde: Nivel de riesgo = <nivel> | Complejidad = <talla>

### Unit Tests — `tests/unit/` ✅ siempre requeridos
Herramienta: `pytest` con mocks de repositorios
Cobertura mínima: <% según matriz>

Casos obligatorios por cada caso de uso:
- [ ] `test_<usecase>_<happy_path>_returns_expected_result`
- [ ] `test_<usecase>_<br_violation>_raises_business_rule_violation` *(uno por cada BR-XXX aplicable)*
- [ ] `test_<usecase>_missing_required_field_raises_validation_error`
- [ ] `test_<usecase>_wrong_organization_raises_authorization_error` *(BR-016)*

### Integration Tests — `tests/integration/` <✅ si Medium/High/Critical | ❌ si Low>
Herramienta: `pytest` + `testcontainers`

- [ ] `test_<entity>_repository_save_and_retrieve`
- [ ] `test_<entity>_repository_filters_by_organization_id`
- [ ] `test_<entity>_repository_excludes_soft_deleted`
- [ ] `test_uow_commit_persists_changes`
- [ ] `test_uow_rollback_reverts_changes`
- [ ] `test_endpoint_<method>_returns_<status>` *(httpx.AsyncClient)*
- [ ] `test_endpoint_without_auth_returns_401`
- [ ] `test_endpoint_wrong_role_returns_403`

### Contract Tests — `tests/contract/` <✅ si High/Critical | ❌ si Low/Medium>
Herramienta: `schemathesis`

- [ ] `test_<module>_openapi_schema_is_valid`
- [ ] `test_<endpoint>_response_matches_contract`

### E2E Tests — `tests/e2e/` <✅ si Critical | ❌ si Low/Medium/High>
Herramienta: `Playwright`

- [ ] `test_<flow>_complete_happy_path`
- [ ] `test_<flow>_handles_error_state`

### Security Tests <✅ si High/Critical | ❌ si Low/Medium>
- [ ] `bandit` sin findings HIGH/CRITICAL
- [ ] `pip-audit` sin vulnerabilidades conocidas
- [ ] `test_cross_tenant_access_returns_403`

## Git Branch
`feature/<feature-name>-backend`
```

## Paso 5 — Ticket Frontend

Plantilla para `tickets/frontend/ticket.md`:

```markdown
---
status: todo
type: frontend
story: <ruta al UserStory.md>
depends-on: tickets/backend/ticket.md
---

# [FE] <Feature Name>

## Objetivo
<UI, flujo de usuario y componentes a implementar>

## Scope
Next.js 15 App Router, features/, components/, TanStack Query, Zod. Sin schema SQL, sin lógica de API.

## Dependencia
Endpoint backend disponible y contrato OpenAPI aprobado.

## Contrato API Consumido
**Endpoint:** <METHOD> /api/v1/<resource>/
<copiar del ticket backend>

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/<role>/<route>/
    page.tsx             - CREATE
    loading.tsx          - CREATE (si aplica)
    error.tsx            - CREATE (si aplica)
  features/<module>/
    components/
      <FeatureComponent>.tsx   - CREATE
    hooks/
      use<Feature>.ts          - CREATE
    schemas/
      <feature>-schema.ts      - CREATE (Zod)
    services/
      <feature>-service.ts     - CREATE/MODIFY
```

## Componentes UI
- <ComponentName> — descripción, props, comportamiento

## Gestión de Estado
- TanStack Query: `useQuery` para <recurso>, `useMutation` para <acción>
- Zustand: solo si hay estado UI local (modales, filtros)

## Validación de Formulario (Zod)
```typescript
const <feature>Schema = z.object({
  // campos con tipos y validaciones
})
```

## Tests Requeridos

> Generado automáticamente desde: Nivel de riesgo = <nivel> | Complejidad = <talla>

### Unit / Component Tests — `tests/` ✅ siempre requeridos
Herramienta: `vitest` + `@testing-library/react`

- [ ] `test_<Component>_renders_without_errors`
- [ ] `test_<Component>_shows_loading_state`
- [ ] `test_<Component>_shows_error_state`
- [ ] `test_<Component>_shows_success_state_with_data`
- [ ] `test_<form>_zod_validation_rejects_invalid_input` *(si hay formulario)*
- [ ] `test_<form>_zod_validation_accepts_valid_input` *(si hay formulario)*

### E2E Tests <✅ si Critical | ❌ si Low/Medium/High>
Herramienta: `Playwright`

- [ ] `test_<flow>_complete_user_journey`
- [ ] `test_<flow>_unauthenticated_redirects_to_login`

## Accesibilidad
- [ ] HTML semántico
- [ ] aria-labels en inputs
- [ ] Navegación por teclado

## Git Branch
`feature/<feature-name>-frontend`
```

## Paso 6 — Confirmar

Responde con la lista de tickets creados y sus rutas. Siguiente paso sugerido: `/create-plan <story-id>`


**Prompt 2:**

**Prompt 3:**

---

### 7. Pull Requests

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**