# Async Processing

## Objetivo

Definir procesamiento asíncrono para tareas no críticas.

## MVP

Procesamiento síncrono.

## Evolución

Redis + Workers

## Casos de Uso

- Generación CRS masiva
- Reportes
- IA Insights
- Notificaciones

## Flujo

Evento
  ↓
Queue
  ↓
Worker
  ↓
Resultado
