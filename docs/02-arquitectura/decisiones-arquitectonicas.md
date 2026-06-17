# Decisiones Arquitectónicas (ADR)

## ADR-001: Monolito Modular

### Estado
Aceptada

### Contexto
El producto inicia como MVP para equipos pequeños y medianos. Se requiere velocidad de desarrollo y baja complejidad operativa.

### Alternativas Evaluadas
- Microservicios
- Monolito tradicional
- Monolito modular

### Decisión
Adoptar un Monolito Modular con límites claros entre dominios.

### Consecuencias Positivas
- Desarrollo más rápido.
- Menor complejidad operativa.
- Menor costo de infraestructura.
- Fácil despliegue con Docker Compose.

### Consecuencias Negativas
- Escalamiento menos granular.
- Mayor disciplina requerida para evitar acoplamiento.

---

## ADR-002: FastAPI como Backend

### Estado
Aceptada

### Alternativas
- Django
- Flask
- Spring Boot

### Decisión
Utilizar FastAPI.

### Justificación
- Excelente rendimiento.
- Tipado fuerte.
- OpenAPI nativo.
- Productividad elevada.

---

## ADR-003: PostgreSQL

### Estado
Aceptada

### Alternativas
- MySQL
- MongoDB

### Decisión
Utilizar PostgreSQL.

### Justificación
- Integridad transaccional.
- Modelo relacional adecuado para CRS.
- Excelente soporte analítico.

---

## ADR-004: Redis

### Estado
Aceptada

### Objetivo
Introducir una capa de cache y preparar futuras capacidades de procesamiento asíncrono.

### Beneficios
- Menor latencia.
- Menor carga en PostgreSQL.

---

## ADR-005: AI Gateway

### Estado
Aceptada

### Problema
Evitar dependencia directa de proveedores de IA.

### Decisión
Implementar AI Gateway.

### Beneficios
- Cambio transparente de proveedor.
- Gestión centralizada de prompts.
- Control de costos.

---

## ADR-006: Docker Compose para MVP

### Estado
Aceptada

### Alternativas
- Kubernetes
- Docker Swarm

### Decisión
Docker Compose.

### Beneficios
- Simplicidad.
- Menor costo.
- Curva de aprendizaje reducida.

---

## ADR-007: Logging First

### Estado
Aceptada

### Decisión
Incorporar logging estructurado desde la primera versión.

### Beneficios
- Diagnóstico temprano.
- Preparación para OpenTelemetry.
