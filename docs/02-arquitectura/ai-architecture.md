# Arquitectura de Inteligencia Artificial

## Objetivo
Definir la arquitectura, principios, responsabilidades y evolución de las capacidades de IA dentro de Priorities Tracker.

## Principios Arquitectónicos
- IA como asistente, no como reemplazo del manager.
- Desacoplamiento de proveedores.
- Fail Safe: la IA nunca bloquea la operación principal.

## Arquitectura

```mermaid
flowchart LR
manager[Manager] --> reports[Reporting Module]
reports --> insights[AI Insights Module]
insights --> gateway[AI Gateway]
gateway --> provider[LLM Provider]
```

## Componentes
### AI Insights Module
- Preparar contexto.
- Construir solicitudes.
- Consumir respuestas.

### AI Gateway
- Routing.
- Control de costos.
- Retries.
- Observabilidad.
- Gestión de prompts.

### Provider Adapter
- OpenAI.
- Anthropic.
- Ollama (futuro).

## Casos de Uso MVP
- Resumen Check-In.
- Resumen Check-Out.
- Detección de Riesgos.
- Preparación de reuniones 1:1.

## Observabilidad IA
- Tokens consumidos.
- Costos.
- Latencia.
- Errores.

## Evolución
- Multi-provider.
- RAG.
- Semantic Search.
- Fine Tuning.
