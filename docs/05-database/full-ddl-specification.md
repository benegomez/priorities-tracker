# Full DDL Specification

## Estándares
- UUID PK
- TIMESTAMPTZ
- Soft Delete
- Audit Columns

## Tabla priorities
- id UUID PK
- organization_id UUID NOT NULL
- phase_id UUID NOT NULL
- owner_id UUID NOT NULL
- title VARCHAR(300) NOT NULL
- description TEXT NULL
- status VARCHAR(30) NOT NULL
- week_period DATE NOT NULL
- created_at TIMESTAMPTZ NOT NULL
- updated_at TIMESTAMPTZ NOT NULL

## Tabla crs_scores
- id UUID PK
- organization_id UUID NOT NULL
- employee_id UUID NOT NULL
- week_period DATE NOT NULL
- score NUMERIC(5,2) NOT NULL
- trend VARCHAR(20) NOT NULL
- risk_level VARCHAR(20) NOT NULL
