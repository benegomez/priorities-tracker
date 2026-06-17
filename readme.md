## Índice

0. [Ficha del proyecto](#0-ficha-del-proyecto)
1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Modelo de datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de usuario](#5-historias-de-usuario)
6. [Tickets de trabajo](#6-tickets-de-trabajo)
7. [Pull requests](#7-pull-requests)

---

## 0. Ficha del proyecto

### **0.1. Tu nombre completo:**
WALTER BENE GOMEZ BELLO

### **0.2. Nombre del proyecto:**
Priorities Tracker

### **0.3. Descripción breve del proyecto:**
Priorities Tracker es una plataforma SaaS que ayuda a managers y equipos a dar seguimiento a prioridades y compromisos semanales. Los colaboradores registran sus objetivos en minutos mediante check-ins simples, mientras los managers obtienen visibilidad del avance, riesgos y cumplimiento a través de métricas e indicadores de desempeño.

Priorities Tracker ayuda a los managers a conocer en qué está trabajando su equipo, qué compromisos se están cumpliendo y qué riesgos requieren atención. A través de check-ins y check-outs semanales simples, la plataforma genera visibilidad, mejora la alineación y permite medir la confiabilidad de ejecución mediante el Commitment Reliability Score (CRS).

### **0.4. URL del proyecto:**

> Puede ser pública o privada, en cuyo caso deberás compartir los accesos de manera segura. Puedes enviarlos a [alvaro@lidr.co](mailto:alvaro@lidr.co) usando algún servicio como [onetimesecret](https://onetimesecret.com/).

### 0.5. URL o archivo comprimido del repositorio

> Puedes tenerlo alojado en público o en privado, en cuyo caso deberás compartir los accesos de manera segura. Puedes enviarlos a [alvaro@lidr.co](mailto:alvaro@lidr.co) usando algún servicio como [onetimesecret](https://onetimesecret.com/). También puedes compartir por correo un archivo zip con el contenido


---

## 1. Descripción general del producto

> Describe en detalle los siguientes aspectos del producto:

### **1.1. Objetivo:**

Crear la plataforma más simple y efectiva para que managers de equipos pequeños obtengan visibilidad real sobre los compromisos, prioridades y capacidad de ejecución de sus colaboradores, sin necesidad de microgestión ni reuniones constantes de seguimiento.

La plataforma responde tres preguntas fundamentales:

1. ¿En qué se comprometió a trabajar cada persona?
2. ¿Qué logró completar?
3. ¿Qué tan confiable es su cumplimiento a lo largo del tiempo?

A diferencia de herramientas de gestión de proyectos, la plataforma no busca administrar tareas complejas, dependencias o cronogramas extensos. Su enfoque es capturar y medir compromisos semanales de forma ligera y consistente.

---

#### Problema que Resuelve

En equipos pequeños existe un vacío entre:

- Herramientas de gestión de proyectos (Asana, Jira, Monday).
- Herramientas de comunicación (Slack, Teams).
- Reuniones de seguimiento.

Los managers frecuentemente enfrentan:

- Falta de visibilidad del trabajo real.
- Dificultad para identificar riesgos tempranos.
- Dependencia excesiva de reuniones de status.
- Poca claridad sobre quién cumple consistentemente.
- Ausencia de métricas objetivas de cumplimiento.

La mayoría de herramientas muestran actividades. Pocas muestran confiabilidad de ejecución.

---

#### Principios del Producto

| Principio | Descripción |
|---|---|
| Simplicidad extrema | Un empleado debe poder completar su Check-In en menos de 5 minutos |
| Seguimiento de compromisos | El foco no son las tareas, sino el compromiso adquirido |
| Consistencia sobre productividad | No se miden horas trabajadas, se mide cumplimiento consistente |
| Conversaciones más inteligentes | La plataforma prepara a managers para seguimientos más efectivos |
| Visibilidad sin microgestión | El manager entiende el estado del equipo sin pedir reportes constantemente |

---

#### Propuesta de Valor

**Para Managers:**
> "Obtén visibilidad inmediata de las prioridades y compromisos de tu equipo, identifica riesgos antes de que se conviertan en problemas y mejora la calidad de tus reuniones de seguimiento."

- Menos tiempo recopilando status.
- Mejor preparación para 1:1.
- Detección temprana de riesgos.
- Métricas objetivas de cumplimiento.
- Mayor claridad sobre capacidad de ejecución.

**Para Empleados:**
> "Comparte tus prioridades semanales en minutos y evita reportes repetitivos o reuniones de actualización innecesarias."

- Menos interrupciones.
- Menos reuniones de status.
- Claridad sobre compromisos.
- Historial de logros.
- Seguimiento simple de prioridades.

**Para Empresas:**
> "Construye equipos más alineados y predecibles mediante visibilidad continua del cumplimiento de compromisos."

- Mejor ejecución.
- Menor dependencia de seguimiento manual.
- Información consistente para evaluaciones.
- Mayor transparencia organizacional.

---

#### Diferenciador Principal: Commitment Reliability Score (CRS)

La mayoría de herramientas responden: *¿Qué está haciendo una persona?*

El CRS responde: *¿Qué tan confiable es una persona para cumplir lo que promete?*

Esto crea una capa de inteligencia organizacional difícil de replicar.

---

#### User Personas

**Persona 1: Manager de Equipo Pequeño**

| Aspecto | Detalle |
|---|---|
| Perfil | Lidera entre 5 y 15 personas. Participa activamente en la operación. Poco tiempo para seguimiento |
| Objetivos | Entender rápidamente el estado del equipo. Identificar riesgos. Reducir reuniones innecesarias |
| Frustraciones | Preguntar constantemente avances. Información dispersa. Sorpresas al final de proyectos |
| Métrica de éxito | Saber en menos de 5 minutos qué hace cada persona, qué está en riesgo y qué requiere atención |

**Persona 2: Colaborador Individual**

| Aspecto | Detalle |
|---|---|
| Perfil | Profesional en uno o varios proyectos. Tiene autonomía para definir prioridades |
| Objetivos | Mantener alineado a su manager. Claridad sobre compromisos. Evitar reportes repetitivos |
| Frustraciones | Reuniones de status poco productivas. Solicitudes constantes de actualización |
| Métrica de éxito | Completar check-in y check-out en pocos minutos |

**Persona 3: Líder de Área**

| Aspecto | Detalle |
|---|---|
| Perfil | Supervisa varios managers. Busca tendencias generales |
| Objetivos | Entender desempeño agregado. Detectar equipos en riesgo. Monitorear capacidad de ejecución |
| Frustraciones | Información inconsistente entre equipos. Falta de indicadores homogéneos |
| Métrica de éxito | Obtener visibilidad consolidada sin revisar cada proyecto |


### **1.2. Características y funcionalidades principales:**

Las funcionalidades se mantienen alineadas con el objetivo principal del producto: seguimiento de prioridades y cumplimiento de compromisos semanales, evitando convertirse en otro gestor de proyectos.

---

#### 1. Gestión Organizacional

**Gestión de Usuarios** — Permite administrar los usuarios de la plataforma.

- Alta, edición y activación/desactivación de usuarios.
- Asignación de roles (Administrador, Manager, Empleado).
- Asignación a equipos y manager.

**Gestión de Equipos**

- Crear y editar equipos.
- Asignar colaboradores y managers.
- Visualizar estructura del equipo.

---

#### 2. Gestión de Proyectos

La finalidad es clasificar prioridades, no administrar proyectos complejos.

**Proyectos**

- Crear, editar, activar/desactivar proyecto.
- Asignar participantes.
- Datos: Nombre, Descripción, Estado, Responsable.

**Fases de Proyecto** — Permite categorizar el trabajo dentro de un proyecto.

- Crear y editar fases.
- Asociar prioridades a fases.
- Ejemplo: Proyecto "Implementación CRM" → Fases: Descubrimiento, Diseño, Desarrollo, Pruebas, Implementación.

---

#### 3. Check-In Semanal

Es la funcionalidad principal del producto. Objetivo: registrar compromisos para la semana.

**Flujo del colaborador:**

1. Selecciona proyectos y fases.
2. Define prioridades y tareas.
3. Selecciona prioridades pendientes.
4. Registra riesgos previstos.
5. Envía check-in.

**Gestión de Prioridades:**

- Crear, editar, duplicar prioridad.
- Reutilizar prioridad de semana anterior.
- Asociar a proyecto y fase.
- Datos: Nombre, Descripción, Proyecto, Fase, Nivel de prioridad, Estado.

**Gestión de Tareas:**

- Crear, editar, marcar completada.
- Mover a siguiente semana.
- Datos: Nombre, Descripción, Estado.

---

#### 4. Seguimiento Durante la Semana

**Actualización de Avance** — Permite registrar progreso sin esperar al cierre semanal.

- Actualizar estado.
- Agregar comentarios y notas.

**Registro de Bloqueadores:**

- Registrar bloqueador y clasificar severidad.
- Marcar resuelto.
- Categorías: Dependencia externa, Falta de información, Problema técnico, Prioridad cambiante, Aprobación pendiente.

**Registro de Riesgos** — Permite anticipar problemas.

- Crear, actualizar y marcar mitigado.

---

#### 5. Check-Out Semanal

Segunda funcionalidad más importante. Objetivo: registrar resultados obtenidos.

**Flujo del colaborador:**

1. Revisa prioridades y marca completadas.
2. Marca tareas completadas.
3. Registra comentarios y aprendizajes.
4. Registra bloqueadores.
5. Define elementos que continúan.
6. Envía check-out.

**Continuidad Automática** — Reduce significativamente la fricción:

- Arrastrar prioridades y tareas pendientes.
- Crear borrador del siguiente check-in.

---

#### 6. Dashboard del Colaborador

Da visibilidad de compromisos y resultados personales.

| Sección | Contenido |
|---|---|
| Mis prioridades actuales | Prioridades activas y su estado |
| Próximo Check-In | Pendientes por registrar |
| Historial | Semanas anteriores |
| Cumplimiento | Tendencia personal y CRS individual |

---

#### 7. Dashboard del Manager

Visibilidad rápida del equipo.

| Vista | Muestra |
|---|---|
| Vista del Equipo | Colaborador, prioridades activas/completadas, bloqueadores, CRS |
| Vista Semanal | Quién hizo check-in/check-out, prioridades, riesgos |
| Vista por Proyecto | Proyecto, prioridades asociadas, estado general, riesgos |

---

#### 8. Commitment Reliability Score (CRS)

Funcionalidad insignia y principal diferenciador del producto. Mide confiabilidad de cumplimiento.

**Variables consideradas:**

- Prioridades comprometidas vs. completadas.
- Tareas comprometidas vs. completadas.
- Prioridades arrastradas.
- Consistencia histórica.

**Resultado:** Score de 0 a 100.

| Rango | Interpretación |
|---|---|
| 90-100 | Cumplimiento excelente |
| 80-89 | Cumplimiento sólido |
| 70-79 | Atención preventiva |
| < 70 | Requiere seguimiento |

---

#### 9. Reportes

| Reporte | Contenido |
|---|---|
| Individual | Historial de prioridades, historial de cumplimiento, evolución CRS |
| De Equipo | Cumplimiento promedio, tendencia semanal, riesgos abiertos, bloqueadores recurrentes |
| De Proyecto | Prioridades activas/completadas, riesgos, cumplimiento |

---

#### 10. Asistente de IA (Complementario)

**Resumen Semanal Automático:**
> "Esta semana el equipo completó el 87% de sus compromisos. Se detectaron 3 prioridades en riesgo y 2 bloqueadores recurrentes."

**Preparación de 1:1** — Genera automáticamente: prioridades completadas, pendientes, riesgos, variación del CRS.

**Insights para Managers:**
- "Juan ha trasladado prioridades durante 4 semanas consecutivas."
- "Ana mantiene un CRS superior a 90 durante 8 semanas."
- "El proyecto CRM concentra el 60% de los bloqueadores del equipo."

---

#### Funcionalidades MVP (Primera Versión)

| Área | Funcionalidades |
|---|---|
| Administración | Usuarios, Equipos, Proyectos, Fases |
| Colaborador | Check-In, Check-Out, Prioridades, Tareas, Continuidad automática |
| Manager | Dashboard de equipo, Vista semanal, Vista individual |
| Métricas | Cumplimiento semanal, CRS |
| IA | Resumen semanal automático |

Todo lo demás puede evolucionar en una V2. Esto mantiene el producto enfocado, simple y alineado con su propuesta de valor principal.


### **1.3. Diseño y experiencia de usuario:**

> Proporciona imágenes y/o videotutorial mostrando la experiencia del usuario desde que aterriza en la aplicación, pasando por todas las funcionalidades principales.

### **1.4. Instrucciones de instalación:**
> Documenta de manera precisa las instrucciones para instalar y poner en marcha el proyecto en local (librerías, backend, frontend, servidor, base de datos, migraciones y semillas de datos, etc.)

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**
> Usa el formato que consideres más adecuado para representar los componentes principales de la aplicación y las tecnologías utilizadas. Explica si sigue algún patrón predefinido, justifica por qué se ha elegido esta arquitectura, y destaca los beneficios principales que aportan al proyecto y justifican su uso, así como sacrificios o déficits que implica.
Arquitectura General

PrioritiesTracker adopta una arquitectura Modular Monolith basada en principios de Domain-Driven Design (DDD), implementada mediante una aplicación web desacoplada en capas lógicas y organizada en contextos de negocio claramente definidos.

Componentes Principales
┌──────────────────────────────┐
│         Frontend             │
│ React + Next.js + TypeScript │
└──────────────┬───────────────┘
               │ HTTPS / REST
               ▼
┌──────────────────────────────┐
│           Backend            │
│      FastAPI (Python)        │
│                              │
│  ┌────────────────────────┐  │
│  │ Organization Context   │  │
│  ├────────────────────────┤  │
│  │ Commitment Context     │  │
│  ├────────────────────────┤  │
│  │ Execution Context      │  │
│  ├────────────────────────┤  │
│  │ Reliability Context    │  │
│  └────────────────────────┘  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         PostgreSQL           │
│     Persistencia de Datos    │
└──────────────────────────────┘



Patrón Arquitectónico

La solución sigue principalmente los siguientes patrones:

Modular Monolith

La plataforma se implementa como una única unidad desplegable organizada internamente en módulos de negocio independientes (Bounded Contexts).

Domain-Driven Design (DDD)

La estructura funcional se organiza alrededor de dominios de negocio:

* Organization
* Commitment
* Execution
* Reliability

Cada dominio posee sus propias reglas de negocio, modelos de datos y APIs.

API First + Contract First

Las APIs son diseñadas antes de su implementación y formalizadas mediante contratos OpenAPI que funcionan como fuente de verdad para consumidores e implementadores.

⸻

Justificación de la Arquitectura Seleccionada

La arquitectura fue seleccionada para maximizar la velocidad de entrega, la mantenibilidad y la simplicidad operacional durante las primeras etapas de evolución del producto.

La evaluación arquitectónica concluyó que una arquitectura de microservicios introduciría complejidad operacional innecesaria para el volumen esperado de usuarios y transacciones durante las fases iniciales del producto.

El enfoque Modular Monolith permite:

* Separación clara de dominios de negocio.
* Menor complejidad operacional.
* Menor costo de infraestructura.
* Despliegues simplificados.
* Mayor velocidad de desarrollo.
* Menor esfuerzo de observabilidad y monitoreo.
* Evolución futura hacia servicios independientes si el crecimiento del producto lo requiere.

⸻

Beneficios Principales

Beneficios Técnicos

* Arquitectura alineada con el dominio de negocio.
* Menor acoplamiento entre capacidades funcionales.
* Simplificación del ciclo de despliegue.
* Menor superficie operativa.
* Facilidad para pruebas automatizadas.
* Facilidad para implementar gobierno arquitectónico.

Beneficios de Negocio

* Reducción de tiempo de entrega.
* Menor costo de mantenimiento.
* Menor costo de infraestructura.
* Menor riesgo de fallas operativas.
* Evolución incremental controlada.

⸻

Sacrificios y Limitaciones

La decisión también implica ciertos compromisos arquitectónicos:

Escalabilidad Independiente Limitada

Los módulos no pueden escalarse de manera independiente mientras permanezcan dentro del monolito.

Ciclo de Despliegue Compartido

Todos los dominios participan en el mismo ciclo de despliegue.

Base de Datos Compartida

Aunque existe propiedad lógica por dominio, la plataforma utiliza una única instancia PostgreSQL.

Evolución a Microservicios

Si el crecimiento futuro lo justifica, será necesario realizar una extracción controlada de dominios hacia servicios independientes.

No obstante, la arquitectura fue diseñada desde el inicio para permitir esta evolución mediante límites de contexto explícitos y contratos API gobernados.

⸻

Referencias Arquitectónicas

Documentos relacionados:

docs/02-arquitectura/ADR/ADR-003-Platform-Strategy-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-006-Backend-Technology-Stack-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-007-Frontend-Technology-Stack-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-010-Domain-Driven-Design-Strategy-Enterprise-Final.md
docs/02-arquitectura/domain/bounded-context-map-v1.0-FINAL.md


### **2.2. Descripción de componentes principales:**

> Describe los componentes más importantes, incluyendo la tecnología utilizada
Descripción de Componentes Principales

La solución PrioritiesTracker está compuesta por los siguientes componentes principales:

1. Frontend Web

Descripción

Aplicación web utilizada por usuarios finales para gestionar compromisos, objetivos, iniciativas, actividades de ejecución y métricas de confiabilidad.

Tecnologías

* React
* Next.js
* TypeScript

Responsabilidades

* Presentación de información.
* Gestión de interacción con usuarios.
* Visualización de dashboards y reportes.
* Consumo de APIs REST.
* Validación básica de formularios.
* Gestión de sesiones de usuario.

⸻

2. API Backend

Descripción

Componente central que implementa la lógica de negocio de la plataforma y expone las capacidades funcionales mediante APIs REST.

Tecnologías

* Python
* FastAPI
* SQLAlchemy
* Alembic

Responsabilidades

* Exposición de APIs.
* Validación de solicitudes.
* Aplicación de reglas de negocio.
* Gestión de autenticación y autorización.
* Orquestación de operaciones de negocio.
* Integración con servicios externos futuros.

⸻

3. Módulos de Dominio (Bounded Contexts)

El backend se encuentra organizado siguiendo principios de Domain-Driven Design (DDD) mediante contextos de negocio independientes.

Organization Context

Responsable de:

* Equipos
* Departamentos
* Roles
* Estructura organizacional

Commitment Context

Responsable de:

* Objetivos
* Prioridades
* Compromisos
* Iniciativas

Execution Context

Responsable de:

* Actividades
* Entregables
* Seguimiento de avance
* Estado de ejecución

Reliability Context

Responsable de:

* Indicadores KPI
* Métricas de confiabilidad
* Dashboards
* Reportes de desempeño

⸻

4. Base de Datos

Descripción

Componente encargado de la persistencia transaccional de la información de negocio.

Tecnología

* PostgreSQL

Responsabilidades

* Almacenamiento persistente.
* Integridad transaccional.
* Consultas operativas.
* Gestión histórica de información.

⸻

5. Gestión de Contratos API

Descripción

Mecanismo de definición y gobierno de interfaces expuestas por la plataforma.

Tecnología

* OpenAPI 3.x

Responsabilidades

* Definición formal de contratos.
* Documentación automática.
* Validación de compatibilidad.
* Gobierno de APIs.

⸻

6. Plataforma de Contenedores

Descripción

Infraestructura de ejecución de la solución.

Tecnologías

* Docker
* Docker Compose

Responsabilidades

* Empaquetado de componentes.
* Consistencia entre ambientes.
* Despliegue reproducible.
* Portabilidad de la plataforma.

⸻

7. Pipeline de Integración y Entrega Continua

Descripción

Automatización del ciclo de construcción, validación y despliegue.

Tecnología

* GitLab CI/CD

Responsabilidades

* Compilación automatizada.
* Ejecución de pruebas.
* Validaciones de calidad.
* Gestión de despliegues.

⸻

8. Componentes de Observabilidad

Descripción

Capacidades transversales para monitoreo y soporte operativo.

Tecnologías

* Logging estructurado
* Health Checks
* Métricas de aplicación

Responsabilidades

* Monitoreo de salud.
* Diagnóstico de incidentes.
* Auditoría operativa.
* Seguimiento de desempeño.

⸻

Referencias

Documentación detallada disponible en:

docs/02-arquitectura/ADR/ADR-006-Backend-Technology-Stack-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-007-Frontend-Technology-Stack-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-010-Domain-Driven-Design-Strategy-Enterprise-Final.md
docs/02-arquitectura/domain/bounded-context-map-v1.0-FINAL.md
docs/03-backend/backend-overview.md



### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

> Representa la estructura del proyecto y explica brevemente el propósito de las carpetas principales, así como si obedece a algún patrón o arquitectura específica.

Descripción de Alto Nivel del Proyecto y Estructura de Ficheros

Descripción General

PrioritiesTracker es una plataforma web orientada a la gestión de objetivos, compromisos, ejecución y medición de resultados organizacionales.

La solución sigue una arquitectura Modular Monolith basada en principios de Domain-Driven Design (DDD), donde las capacidades funcionales se organizan alrededor de dominios de negocio claramente definidos.

El repositorio se estructura como un Monorepo, permitiendo gestionar de forma centralizada la aplicación frontend, backend, documentación, automatización e infraestructura.

⸻

Estructura General del Proyecto

priorities-tracker/
│
├── apps/
│   ├── frontend/
│   └── backend/
│
├── docs/
│
├── infrastructure/
│
├── scripts/
│
├── tests/
│
├── .gitlab/
│
├── docker/
│
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE

⸻

Descripción de Carpetas Principales

apps/

Contiene el código fuente de las aplicaciones principales.

apps/
├── frontend/
└── backend/

⸻

apps/frontend/

Aplicación web utilizada por los usuarios finales.

Tecnologías:

* React
* Next.js
* TypeScript

Responsabilidades:

* Interfaz de usuario.
* Visualización de información.
* Dashboards.
* Formularios.
* Consumo de APIs REST.

Ejemplo:

frontend/
├── app/
├── components/
├── features/
├── services/
├── hooks/
└── styles/

⸻

apps/backend/

Implementación de la lógica de negocio y exposición de APIs.

Tecnologías:

* Python
* FastAPI
* SQLAlchemy
* Alembic

Responsabilidades:

* Reglas de negocio.
* Persistencia.
* Seguridad.
* APIs REST.
* Integraciones.

Ejemplo:

backend/
├── organization/
├── commitment/
├── execution/
├── reliability/
├── shared/
└── api/

⸻

docs/

Repositorio documental del proyecto.

Contiene arquitectura, gobierno, estándares y documentación funcional.

docs/
├── 01-product/
├── 02-arquitectura/
├── 03-engineering/
├── 04-operaciones/
└── 05-governance/

Responsabilidades:

* Arquitectura empresarial.
* ADRs.
* Gobierno técnico.
* Procedimientos operativos.
* Estándares de desarrollo.

⸻

infrastructure/

Artefactos de infraestructura como código.

Ejemplos:

infrastructure/
├── docker/
├── environments/
├── deployments/
└── monitoring/

Responsabilidades:

* Configuración de despliegues.
* Infraestructura reproducible.
* Automatización operativa.

⸻

tests/

Pruebas automatizadas de la plataforma.

tests/
├── unit/
├── integration/
├── contract/
└── e2e/

Responsabilidades:

* Validación funcional.
* Validación de integración.
* Validación de contratos API.
* Validación end-to-end.

⸻

scripts/

Automatizaciones y utilidades de soporte.

Ejemplos:

* Migraciones.
* Carga de datos.
* Mantenimiento.
* Herramientas administrativas.

⸻

docker/

Configuraciones de contenedores.

Ejemplos:

* Dockerfiles
* Scripts de inicialización
* Configuración de imágenes

⸻

.gitlab/

Configuración de CI/CD.

Responsabilidades:

* Pipelines.
* Quality Gates.
* Seguridad.
* Automatización de despliegues.

⸻

Patrón Arquitectónico Utilizado

La estructura del proyecto sigue una combinación de patrones arquitectónicos:

Monorepo

Todo el código fuente, documentación e infraestructura se administran desde un único repositorio.

Beneficios:

* Gobierno simplificado.
* Trazabilidad.
* Versionado consistente.
* Menor complejidad operativa.

⸻

Modular Monolith

La aplicación se despliega como una única unidad lógica pero organizada internamente por dominios independientes.

Beneficios:

* Menor complejidad que microservicios.
* Separación clara de responsabilidades.
* Evolución controlada.

⸻

Domain-Driven Design (DDD)

La organización interna del backend se basa en contextos de negocio:

* Organization
* Commitment
* Execution
* Reliability

Beneficios:

* Alineación con el negocio.
* Propiedad clara de dominios.
* Escalabilidad organizacional.

⸻

API First + Contract First

Las APIs y contratos OpenAPI son diseñados antes de la implementación.

Beneficios:

* Integraciones consistentes.
* Mejor mantenibilidad.
* Documentación automática.

⸻

Referencias

Documentación detallada disponible en:

docs/02-arquitectura/ADR/ADR-001-Monorepo-Strategy-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-002-Repository-Strategy-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-003-Platform-Strategy-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-010-Domain-Driven-Design-Strategy-Enterprise-Final.md
docs/02-arquitectura/domain/bounded-context-map-v1.0-FINAL.md
docs/03-backend/project-structure.md

### **2.4. Infraestructura y despliegue**

> Detalla la infraestructura del proyecto, incluyendo un diagrama en el formato que creas conveniente, y explica el proceso de despliegue que se sigue

Infraestructura y Despliegue

Descripción General de la Infraestructura

PrioritiesTracker se despliega utilizando una arquitectura basada en contenedores Docker bajo un modelo Docker Compose First, definido en el ADR-004 (Kubernetes Migration Path).

La solución está compuesta por tres componentes principales:

* Frontend Web
* Backend API
* Base de Datos PostgreSQL

Todos los componentes son desplegados como contenedores independientes y se comunican mediante una red privada interna.

⸻

Diagrama de Infraestructura

                     ┌───────────────────┐
                     │      Usuario      │
                     │ Navegador Web     │
                     └─────────┬─────────┘
                               │ HTTPS
                               ▼
┌──────────────────────────────────────────────────┐
│                 Docker Host                      │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │ Frontend Container                         │  │
│  │ React + Next.js + TypeScript               │  │
│  └────────────────┬───────────────────────────┘  │
│                   │ REST API                      │
│                   ▼                               │
│  ┌────────────────────────────────────────────┐  │
│  │ Backend Container                          │  │
│  │ Python + FastAPI                           │  │
│  │ SQLAlchemy + Alembic                       │  │
│  └────────────────┬───────────────────────────┘  │
│                   │ SQL                          │
│                   ▼                              │
│  ┌────────────────────────────────────────────┐  │
│  │ PostgreSQL Container                       │  │
│  │ Persistencia de Datos                      │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘

⸻

Tecnologías de Infraestructura

Componente	Tecnología
Contenedores	Docker
Orquestación Inicial	Docker Compose
Frontend	React + Next.js
Backend	FastAPI (Python)
Persistencia	PostgreSQL
Control de Versiones	GitLab
CI/CD	GitLab CI/CD
Contratos API	OpenAPI 3.x

⸻

Modelo de Despliegue

La solución sigue un modelo de despliegue centralizado:

Código Fuente
      ↓
GitLab Repository
      ↓
Pipeline CI/CD
      ↓
Build de Imágenes Docker
      ↓
Validación Automatizada
      ↓
Docker Registry
      ↓
Despliegue mediante Docker Compose

⸻

Proceso de Despliegue

1. Desarrollo

Los cambios son implementados por los equipos de desarrollo dentro del repositorio principal (Monorepo).

Cada cambio se asocia a:

* Requerimiento
* Historia de usuario
* Pull Request
* Revisión de código

⸻

2. Integración Continua

Al realizar un commit o merge request se ejecuta automáticamente el pipeline de CI/CD.

Actividades principales:

* Compilación
* Ejecución de pruebas unitarias
* Validación de contratos OpenAPI
* Análisis estático
* Validaciones de seguridad

⸻

3. Construcción de Imágenes

Una vez superadas las validaciones:

* Se generan imágenes Docker versionadas.
* Las imágenes son almacenadas en el registro corporativo.

Ejemplo:

prioritiestracker-frontend:v1.0.0
prioritiestracker-api:v1.0.0

⸻

4. Despliegue

El despliegue se realiza mediante Docker Compose utilizando imágenes previamente validadas.

Componentes desplegados:

* Frontend
* Backend
* PostgreSQL

La configuración de cada entorno se suministra mediante variables de entorno externas.

⸻

5. Validación Post-Despliegue

Posteriormente se ejecutan verificaciones operativas:

* Health Checks
* Verificación de APIs
* Validación de conectividad
* Validación de logs

⸻

Beneficios de la Infraestructura Seleccionada

Simplicidad Operacional

La infraestructura puede ser operada por equipos pequeños sin necesidad de administrar una plataforma de orquestación compleja.

Menor Costo

Reduce significativamente los costos operativos frente a una arquitectura Kubernetes desde etapas tempranas.

Portabilidad

Los contenedores permiten ejecutar la solución de forma consistente en diferentes entornos.

Evolución Controlada

La arquitectura mantiene compatibilidad con una futura migración a Kubernetes sin requerir rediseño de la aplicación.

⸻

Limitaciones y Consideraciones

Escalabilidad Horizontal Limitada

Docker Compose ofrece menos capacidades de escalamiento automático que Kubernetes.

Alta Disponibilidad

La solución inicial no implementa mecanismos avanzados de alta disponibilidad.

Gestión Manual de Infraestructura

Determinadas tareas operativas pueden requerir intervención manual.

Estas limitaciones fueron aceptadas debido a que el volumen esperado de uso no justifica actualmente la complejidad operacional de una plataforma Kubernetes.

⸻

Referencias

Documentación detallada disponible en:

docs/02-arquitectura/ADR/ADR-003-Platform-Strategy-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-004-Kubernetes-Migration-Path-Enterprise-Final.md
docs/04-operaciones/deployment-guide.md
docs/04-operaciones/runbook.md

### **2.5. Seguridad**

> Enumera y describe las prácticas de seguridad principales que se han implementado en el proyecto, añadiendo ejemplos si procede

2.5 Seguridad

Enfoque General

PrioritiesTracker aplica el principio de Security by Design, incorporando controles de seguridad desde las fases de diseño, desarrollo, despliegue y operación de la plataforma.

La estrategia de seguridad se basa en la protección de la confidencialidad, integridad y disponibilidad de la información, así como en la reducción de riesgos operativos y de acceso no autorizado.

⸻

Principales Prácticas de Seguridad Implementadas

1. Autenticación de Usuarios

La plataforma requiere autenticación previa para acceder a funcionalidades protegidas.

Objetivos:

* Verificar la identidad del usuario.
* Impedir accesos no autorizados.
* Proteger recursos sensibles.

Ejemplos:

* Inicio de sesión mediante credenciales corporativas.
* Integración futura con proveedores SSO (OIDC/SAML).
* Tokens de acceso firmados.

⸻

2. Autorización Basada en Roles (RBAC)

El acceso a funcionalidades y datos se controla mediante permisos asociados a roles organizacionales.

Beneficios:

* Principio de mínimo privilegio.
* Segregación de responsabilidades.
* Reducción de accesos indebidos.

Ejemplo:

Administrador
    ├─ Gestión de usuarios
    ├─ Configuración
    └─ Gobierno
Usuario Operativo
    ├─ Consulta
    ├─ Actualización de tareas
    └─ Seguimiento de compromisos

⸻

3. Protección de APIs

Todas las APIs expuestas siguen las directrices definidas en:

* ADR-008 API First Strategy
* ADR-009 OpenAPI Contract First

Controles implementados:

* Autenticación obligatoria.
* Validación de entrada.
* Validación de esquemas.
* Manejo controlado de errores.
* Versionado de APIs.

Ejemplo:

Authorization: Bearer <token>

⸻

4. Validación de Datos de Entrada

Toda información recibida desde interfaces o APIs es validada antes de ser procesada.

Objetivos:

* Evitar datos inconsistentes.
* Mitigar ataques de inyección.
* Reducir errores operativos.

Ejemplos:

* Validación de tipos.
* Restricciones de longitud.
* Validación de formatos.
* Esquemas OpenAPI.

⸻

5. Gestión Segura de Secretos

Las credenciales y configuraciones sensibles no se almacenan en el código fuente.

Prácticas aplicadas:

* Variables de entorno.
* Configuración externa.
* Exclusión de secretos del repositorio.

Ejemplos:

DATABASE_URL
JWT_SECRET
SMTP_PASSWORD
API_KEYS

⸻

6. Cifrado de Comunicaciones

Toda comunicación entre clientes y servicios debe realizarse mediante protocolos seguros.

Controles:

* HTTPS/TLS.
* Certificados digitales válidos.
* Protección de credenciales en tránsito.

Beneficios:

* Protección contra interceptación.
* Protección contra ataques Man-in-the-Middle.

⸻

7. Seguridad en Base de Datos

La persistencia de datos se protege mediante controles de acceso y segregación de responsabilidades.

Prácticas:

* Usuarios con permisos mínimos.
* Accesos restringidos.
* Separación entre entornos.

Beneficios:

* Reducción del riesgo de exposición de datos.
* Protección frente a modificaciones no autorizadas.

⸻

8. Registro y Auditoría

La plataforma genera eventos auditables para actividades relevantes.

Ejemplos:

* Inicio de sesión.
* Modificación de configuraciones.
* Cambios de permisos.
* Actualización de información crítica.

Objetivos:

* Trazabilidad.
* Investigación de incidentes.
* Cumplimiento normativo.

⸻

9. Seguridad en el Ciclo de Desarrollo

El pipeline de integración continua incorpora controles automáticos de calidad y seguridad.

Validaciones:

* Revisión de código.
* Análisis estático.
* Ejecución de pruebas automatizadas.
* Validación de dependencias.

Beneficios:

* Detección temprana de vulnerabilidades.
* Reducción de defectos en producción.

⸻

10. Contenedores y Entornos

La solución se ejecuta mediante contenedores Docker aislados.

Prácticas:

* Imágenes versionadas.
* Configuración externalizada.
* Entornos reproducibles.
* Separación entre desarrollo, pruebas y producción.

⸻

Beneficios de la Estrategia de Seguridad

La adopción de estos controles permite:

* Reducir la superficie de ataque.
* Mejorar la protección de datos.
* Aumentar la trazabilidad operativa.
* Facilitar auditorías y revisiones de cumplimiento.
* Reducir riesgos asociados a errores humanos.
* Mantener una postura de seguridad consistente durante todo el ciclo de vida del producto.

⸻

Referencias

Documentación relacionada:

docs/02-arquitectura/principles/architecture-principles-v1.0-FINAL.md
docs/02-arquitectura/ADR/ADR-008-API-First-Strategy-Enterprise-Final.md
docs/02-arquitectura/ADR/ADR-009-OpenAPI-Contract-First-Enterprise-Final.md
docs/03-backend/api-design.md
docs/09-governance/governance-charter-v1.0-FINAL.md


### **2.6. Tests**

> Describe brevemente algunos de los tests realizados

---

## 3. Modelo de Datos

### **3.1. Diagrama del modelo de datos:**

> Recomendamos usar mermaid para el modelo de datos, y utilizar todos los parámetros que permite la sintaxis para dar el máximo detalle, por ejemplo las claves primarias y foráneas.
3.1 Diagrama del Modelo de Datos

El modelo de datos de PrioritiesTracker está diseñado siguiendo los principios de Domain-Driven Design (DDD) definidos en ADR-010.

Cada entidad pertenece a un contexto de negocio claramente identificado y mantiene relaciones explícitas mediante claves primarias y foráneas.

Modelo de Datos (Mermaid)

erDiagram
    ORGANIZATION {
        UUID id PK
        string name
        string code
        string description
        datetime created_at
        datetime updated_at
    }
    TEAM {
        UUID id PK
        UUID organization_id FK
        string name
        string code
        datetime created_at
        datetime updated_at
    }
    USER {
        UUID id PK
        UUID team_id FK
        string email UK
        string first_name
        string last_name
        string role
        boolean active
        datetime created_at
        datetime updated_at
    }
    COMMITMENT {
        UUID id PK
        UUID owner_team_id FK
        string title
        string description
        string status
        date start_date
        date target_date
        datetime created_at
        datetime updated_at
    }
    OBJECTIVE {
        UUID id PK
        UUID commitment_id FK
        string title
        string description
        string status
        decimal target_value
        datetime created_at
        datetime updated_at
    }
    EXECUTION_ITEM {
        UUID id PK
        UUID objective_id FK
        UUID assigned_user_id FK
        string title
        string description
        string status
        decimal progress_percentage
        date due_date
        datetime created_at
        datetime updated_at
    }
    EXECUTION_UPDATE {
        UUID id PK
        UUID execution_item_id FK
        UUID updated_by FK
        string comment
        decimal progress_percentage
        datetime created_at
    }
    KPI {
        UUID id PK
        UUID objective_id FK
        string name
        string unit
        decimal target_value
        decimal current_value
        datetime created_at
        datetime updated_at
    }
    KPI_MEASUREMENT {
        UUID id PK
        UUID kpi_id FK
        decimal measured_value
        datetime measured_at
        string source
    }
    ORGANIZATION ||--o{ TEAM : contains
    TEAM ||--o{ USER : has
    TEAM ||--o{ COMMITMENT : owns
    COMMITMENT ||--o{ OBJECTIVE : defines
    OBJECTIVE ||--o{ EXECUTION_ITEM : executed_by
    USER ||--o{ EXECUTION_ITEM : assigned_to
    EXECUTION_ITEM ||--o{ EXECUTION_UPDATE : updates
    USER ||--o{ EXECUTION_UPDATE : records
    OBJECTIVE ||--o{ KPI : measured_by
    KPI ||--o{ KPI_MEASUREMENT : captures

⸻

Descripción General del Modelo

El modelo se encuentra dividido en cuatro dominios principales:

Organization Context

Responsable de:

* Organizaciones
* Equipos
* Usuarios
* Estructura organizacional

Entidades:

* ORGANIZATION
* TEAM
* USER

⸻

Commitment Context

Responsable de:

* Compromisos
* Objetivos
* Planeación estratégica

Entidades:

* COMMITMENT
* OBJECTIVE

⸻

Execution Context

Responsable de:

* Actividades
* Entregables
* Seguimiento de avance

Entidades:

* EXECUTION_ITEM
* EXECUTION_UPDATE

⸻

Reliability Context

Responsable de:

* KPIs
* Indicadores
* Medición de resultados

Entidades:

* KPI
* KPI_MEASUREMENT

⸻

Consideraciones de Diseño

Identificadores

Todas las entidades utilizan UUID como clave primaria para facilitar:

* Escalabilidad futura.
* Integraciones.
* Migración potencial a microservicios.

Auditoría

Todas las entidades de negocio incluyen:

* created_at
* updated_at

para garantizar trazabilidad operativa.

Integridad Referencial

Las relaciones se implementan mediante claves foráneas explícitas y restricciones de integridad administradas por PostgreSQL.

Separación por Dominio

Aunque la solución utiliza una única instancia PostgreSQL (ADR-004), la propiedad lógica de datos está delimitada por contexto de negocio siguiendo ADR-010.

⸻

Referencias

* 02-arquitectura/adr/ADR-010-domain-driven-design-strategy.md
* 02-arquitectura/domain/bounded-context-map.md
* 02-arquitectura/adr/ADR-003-platform-strategy.md
* 02-arquitectura/adr/ADR-006-backend-technology-stack.md

:::
**Observación:** este modelo es un **modelo lógico enterprise**, no necesariamente el esquema físico final. Para una licitación o revisión técnica suele ser suficiente. Si después quieres un nivel más detallado, podemos generar una **versión física PostgreSQL** con 20–30 tablas adicionales (audit_log, attachment, comment, notification, tag, objective_history, execution_history, etc.), que es más cercana a lo que terminaría implementándose en producción.

### **3.2. Descripción de entidades principales:**

> Recuerda incluir el máximo detalle de cada entidad, como el nombre y tipo de cada atributo, descripción breve si procede, claves primarias y foráneas, relaciones y tipo de relación, restricciones (unique, not null…), etc.

3.2 Descripción de Entidades Principales

ORGANIZATION

Descripción

Representa una unidad organizacional de alto nivel dentro de la plataforma.

Tabla

ORGANIZATION

Atributos

Campo	Tipo	Restricciones	Descripción
id	UUID	PK, NOT NULL	Identificador único de la organización
name	VARCHAR(200)	NOT NULL	Nombre de la organización
code	VARCHAR(50)	UNIQUE, NOT NULL	Código único organizacional
description	TEXT	NULL	Descripción general
created_at	TIMESTAMP	NOT NULL	Fecha de creación
updated_at	TIMESTAMP	NOT NULL	Fecha de última actualización

Relaciones

Relación	Entidad	Cardinalidad
Tiene	TEAM	1:N

⸻

TEAM

Descripción

Representa equipos funcionales pertenecientes a una organización.

Tabla

TEAM

Atributos

Campo	Tipo	Restricciones	Descripción
id	UUID	PK, NOT NULL	Identificador único
organization_id	UUID	FK, NOT NULL	Organización propietaria
name	VARCHAR(200)	NOT NULL	Nombre del equipo
code	VARCHAR(50)	UNIQUE, NOT NULL	Código del equipo
created_at	TIMESTAMP	NOT NULL	Fecha de creación
updated_at	TIMESTAMP	NOT NULL	Fecha de actualización

Claves Foráneas

organization_id → ORGANIZATION.id

Relaciones

Relación	Entidad	Cardinalidad
Pertenece a	ORGANIZATION	N:1
Contiene	USER	1:N
Responsable de	COMMITMENT	1:N

⸻

USER

Descripción

Representa usuarios internos de la plataforma.

Tabla

USER

Atributos

Campo	Tipo	Restricciones	Descripción
id	UUID	PK, NOT NULL	Identificador único
team_id	UUID	FK, NOT NULL	Equipo al que pertenece
email	VARCHAR(255)	UNIQUE, NOT NULL	Correo electrónico
first_name	VARCHAR(100)	NOT NULL	Nombre
last_name	VARCHAR(100)	NOT NULL	Apellido
role	VARCHAR(50)	NOT NULL	Rol asignado
active	BOOLEAN	NOT NULL	Estado del usuario
created_at	TIMESTAMP	NOT NULL	Fecha de creación
updated_at	TIMESTAMP	NOT NULL	Fecha de actualización

Claves Foráneas

team_id → TEAM.id

Relaciones

Relación	Entidad	Cardinalidad
Pertenece a	TEAM	N:1
Responsable de	EXECUTION_ITEM	1:N
Registra	EXECUTION_UPDATE	1:N

⸻

COMMITMENT

Descripción

Representa compromisos estratégicos definidos por la organización.

Tabla

COMMITMENT

Atributos

Campo	Tipo	Restricciones	Descripción
id	UUID	PK, NOT NULL	Identificador único
owner_team_id	UUID	FK, NOT NULL	Equipo responsable
title	VARCHAR(250)	NOT NULL	Título
description	TEXT	NULL	Descripción
status	VARCHAR(30)	NOT NULL	Estado actual
start_date	DATE	NOT NULL	Fecha inicio
target_date	DATE	NOT NULL	Fecha objetivo
created_at	TIMESTAMP	NOT NULL	Creación
updated_at	TIMESTAMP	NOT NULL	Actualización

Claves Foráneas

owner_team_id → TEAM.id

Relaciones

Relación	Entidad	Cardinalidad
Pertenece a	TEAM	N:1
Contiene	OBJECTIVE	1:N

⸻

OBJECTIVE

Descripción

Representa objetivos específicos asociados a un compromiso.

Tabla

OBJECTIVE

Atributos

Campo	Tipo	Restricciones	Descripción
id	UUID	PK, NOT NULL	Identificador
commitment_id	UUID	FK, NOT NULL	Compromiso asociado
title	VARCHAR(250)	NOT NULL	Nombre
description	TEXT	NULL	Descripción
status	VARCHAR(30)	NOT NULL	Estado
target_value	DECIMAL(18,2)	NULL	Valor objetivo
created_at	TIMESTAMP	NOT NULL	Creación
updated_at	TIMESTAMP	NOT NULL	Actualización

Claves Foráneas

commitment_id → COMMITMENT.id

Relaciones

Relación	Entidad	Cardinalidad
Pertenece a	COMMITMENT	N:1
Contiene	EXECUTION_ITEM	1:N
Contiene	KPI	1:N

⸻

EXECUTION_ITEM

Descripción

Representa una actividad o entregable que contribuye al cumplimiento de un objetivo.

Tabla

EXECUTION_ITEM

Atributos

Campo	Tipo	Restricciones	Descripción
id	UUID	PK, NOT NULL	Identificador
objective_id	UUID	FK, NOT NULL	Objetivo asociado
assigned_user_id	UUID	FK, NOT NULL	Responsable
title	VARCHAR(250)	NOT NULL	Nombre
description	TEXT	NULL	Descripción
status	VARCHAR(30)	NOT NULL	Estado
progress_percentage	DECIMAL(5,2)	CHECK 0-100	Avance
due_date	DATE	NULL	Fecha compromiso
created_at	TIMESTAMP	NOT NULL	Creación
updated_at	TIMESTAMP	NOT NULL	Actualización

Claves Foráneas

objective_id → OBJECTIVE.id
assigned_user_id → USER.id

Relaciones

Relación	Entidad	Cardinalidad
Pertenece a	OBJECTIVE	N:1
Asignado a	USER	N:1
Contiene	EXECUTION_UPDATE	1:N

⸻

KPI

Descripción

Representa un indicador utilizado para medir el desempeño de un objetivo.

Tabla

KPI

Atributos

Campo	Tipo	Restricciones	Descripción
id	UUID	PK, NOT NULL	Identificador
objective_id	UUID	FK, NOT NULL	Objetivo asociado
name	VARCHAR(200)	NOT NULL	Nombre KPI
unit	VARCHAR(30)	NOT NULL	Unidad de medida
target_value	DECIMAL(18,4)	NOT NULL	Meta
current_value	DECIMAL(18,4)	NULL	Valor actual
created_at	TIMESTAMP	NOT NULL	Creación
updated_at	TIMESTAMP	NOT NULL	Actualización

Claves Foráneas

objective_id → OBJECTIVE.id

Relaciones

Relación	Entidad	Cardinalidad
Pertenece a	OBJECTIVE	N:1
Contiene	KPI_MEASUREMENT	1:N

⸻

KPI_MEASUREMENT

Descripción

Histórico de mediciones asociadas a un KPI.

Tabla

KPI_MEASUREMENT

Atributos

Campo	Tipo	Restricciones	Descripción
id	UUID	PK, NOT NULL	Identificador
kpi_id	UUID	FK, NOT NULL	KPI asociado
measured_value	DECIMAL(18,4)	NOT NULL	Valor medido
measured_at	TIMESTAMP	NOT NULL	Fecha medición
source	VARCHAR(100)	NULL	Fuente del dato

Claves Foráneas

kpi_id → KPI.id

Relaciones

Relación	Entidad	Cardinalidad
Pertenece a	KPI	N:1

⸻

Restricciones Globales

Integridad Referencial

Todas las claves foráneas son validadas por PostgreSQL.

Identificadores

Todas las entidades utilizan UUID v4 como clave primaria.

Auditoría

Todas las entidades de negocio mantienen:

created_at
updated_at

Convenciones

* PK → UUID
* FK → UUID
* Fechas → TIMESTAMP UTC
* Estados → Enumeraciones controladas
* Correos electrónicos → UNIQUE
* Códigos de negocio → UNIQUE

---

## 4. Especificación de la API

> Si tu backend se comunica a través de API, describe los endpoints principales (máximo 3) en formato OpenAPI. Opcionalmente puedes añadir un ejemplo de petición y de respuesta para mayor claridad

3.3 Especificación de la API

La plataforma expone APIs REST documentadas mediante OpenAPI 3.x, siguiendo los principios definidos en:

* ADR-008 API First Strategy
* ADR-009 OpenAPI Contract First

A continuación se presentan tres endpoints representativos de los dominios principales de negocio.

⸻

Endpoint 1 - Consultar Compromisos

Descripción

Obtiene la lista de compromisos estratégicos registrados en la plataforma.

OpenAPI

paths:
  /api/v1/commitments:
    get:
      summary: List commitments
      operationId: listCommitments
      responses:
        '200':
          description: Commitments retrieved successfully
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Commitment'

Ejemplo de Petición

GET /api/v1/commitments
Authorization: Bearer <token>

Ejemplo de Respuesta

[
  {
    "id": "8d4b4c52-2baf-4db5-ae3e-ec2a83a8a102",
    "title": "Increase Customer Retention",
    "status": "IN_PROGRESS",
    "targetDate": "2026-12-31"
  }
]

⸻

Endpoint 2 - Actualizar Avance de Ejecución

Descripción

Permite registrar el progreso de una actividad de ejecución.

OpenAPI

paths:
  /api/v1/execution-items/{id}/progress:
    patch:
      summary: Update execution progress
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - progressPercentage
              properties:
                progressPercentage:
                  type: number
                  minimum: 0
                  maximum: 100
      responses:
        '200':
          description: Progress updated successfully

Ejemplo de Petición

PATCH /api/v1/execution-items/1f0f9d0e-c1a4-4ef8-9f2f-912e20fd3321/progress
Authorization: Bearer <token>
Content-Type: application/json
{
  "progressPercentage": 75
}

Ejemplo de Respuesta

{
  "id": "1f0f9d0e-c1a4-4ef8-9f2f-912e20fd3321",
  "progressPercentage": 75,
  "status": "IN_PROGRESS",
  "updatedAt": "2026-06-16T15:30:00Z"
}

⸻

Endpoint 3 - Consultar Indicadores (KPIs)

Descripción

Obtiene los indicadores asociados a un objetivo estratégico.

OpenAPI

paths:
  /api/v1/objectives/{objectiveId}/kpis:
    get:
      summary: Get objective KPIs
      parameters:
        - name: objectiveId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: KPI list retrieved successfully
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/KPI'

Ejemplo de Petición

GET /api/v1/objectives/4c1837aa-8c68-43d2-9ebf-ef5f43e6c201/kpis
Authorization: Bearer <token>

Ejemplo de Respuesta

[
  {
    "id": "7b7fd3f4-cf5c-4f54-b48e-6c4a95f72d31",
    "name": "Customer Retention Rate",
    "targetValue": 95,
    "currentValue": 91.2,
    "unit": "%"
  }
]

⸻

Componentes Principales

components:
  schemas:
    Commitment:
      type: object
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
        status:
          type: string
        targetDate:
          type: string
          format: date
    KPI:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        targetValue:
          type: number
        currentValue:
          type: number
        unit:
          type: string

⸻

Referencias

- docs/02-arquitectura/ADR/ADR-008-API-First-Strategy-Enterprise-Final.md
- docs/02-arquitectura/ADR/ADR-009-OpenAPI-Contract-First-Enterprise-Final.md
- docs/02-arquitectura/domain/bounded-context-map-v1.0-FINAL.md
- docs/03-backend/api-design.md
- docs/06-api-implementation/

---

## 5. Historias de Usuario

> Documenta 3 de las historias de usuario principales utilizadas durante el desarrollo, teniendo en cuenta las buenas prácticas de producto al respecto.

**Historia de Usuario 1**
docs/user-stories/001-weekly-checkin-creation/UserStory.md


**Historia de Usuario 2**

docs/user-stories/002-user-authentication/UserStory.md

**Historia de Usuario 3**

docs/user-stories/003-weekly-checkout/UserStory.md

---

## 6. Tickets de Trabajo

> Documenta 3 de los tickets de trabajo principales del desarrollo, uno de backend, uno de frontend, y uno de bases de datos. Da todo el detalle requerido para desarrollar la tarea de inicio a fin teniendo en cuenta las buenas prácticas al respecto. 

**Ticket 1**
docs/user-stories/001-weekly-checkin-creation/tickets/backend/ticket.md

**Ticket 2**
docs/user-stories/001-weekly-checkin-creation/tickets/database/ticket.md

**Ticket 3**
docs/user-stories/001-weekly-checkin-creation/tickets/frontend/ticket.md
---

## 7. Pull Requests

> Documenta 3 de las Pull Requests realizadas durante la ejecución del proyecto

**Pull Request 1**

**Pull Request 2**

**Pull Request 3**
