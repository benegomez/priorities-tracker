# Project Structure

## Estructura General

src/
├── main.py
├── modules/
│   ├── auth/
│   ├── users/
│   ├── teams/
│   ├── projects/
│   ├── priorities/
│   ├── checkin/
│   ├── checkout/
│   ├── crs/
│   ├── reporting/
│   └── ai_insights/
│
├── shared/
│   ├── database/
│   ├── security/
│   ├── logging/
│   ├── ai/
│   ├── config/
│   └── exceptions/
│
└── tests/

## Estructura Interna de Módulo

api/
application/
domain/
infrastructure/
tests/

## Convención

Cada módulo mantiene su propia Clean Architecture.
