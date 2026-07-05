---
status: done
type: database
story: docs/user-stories/003-weekly-checkout/UserStory.md
depends-on: null
risk_level: Critical
complexity: M
---

# [DB] US-003 — Weekly Check-Out Schema

## Objetivo

Crear las tablas `check_outs` y `crs_scores` que soportan el flujo de cierre semanal y el almacenamiento del CRS calculado.

## Scope

Solo schema PostgreSQL + migración Alembic. Sin endpoints, sin lógica de negocio, sin UI.

---

## Prerequisitos

Las tablas `organizations`, `users`, `check_ins`, `priorities`, `tasks` ya existen (migraciones anteriores).

---

## Cambios al Schema

### Tabla: `check_outs`

```sql
CREATE TABLE check_outs (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES organizations(id),
    employee_id     UUID        NOT NULL REFERENCES users(id),
    checkin_id      UUID        NOT NULL REFERENCES check_ins(id),
    week_start      DATE        NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'draft'
                                CHECK (status IN ('draft', 'submitted', 'closed')),
    submitted_at    TIMESTAMPTZ NULL,
    notes           TEXT        NULL,
    lessons_learned TEXT        NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID        NULL
);
```

**Índices:**
```sql
-- BR-002: un solo check-out activo por empleado por semana
CREATE UNIQUE INDEX uq_check_outs_employee_week
    ON check_outs (employee_id, week_start)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_check_outs_organization_id ON check_outs (organization_id);
CREATE INDEX idx_check_outs_employee_id ON check_outs (employee_id);
CREATE INDEX idx_check_outs_checkin_id ON check_outs (checkin_id);
CREATE INDEX idx_check_outs_week_start ON check_outs (week_start);
```

---

### Tabla: `crs_scores`

```sql
CREATE TABLE crs_scores (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES organizations(id),
    employee_id     UUID        NOT NULL REFERENCES users(id),
    checkout_id     UUID        NOT NULL REFERENCES check_outs(id),
    week_start      DATE        NOT NULL,
    score           NUMERIC(5,2) NOT NULL,
    trend           VARCHAR(20) NOT NULL DEFAULT 'stable'
                                CHECK (trend IN ('improving', 'stable', 'declining')),
    risk_level      VARCHAR(20) NOT NULL DEFAULT 'low'
                                CHECK (risk_level IN ('low', 'moderate', 'high')),
    formula_version VARCHAR(10) NOT NULL DEFAULT 'v1.0',
    priorities_total     INT NOT NULL DEFAULT 0,
    priorities_completed INT NOT NULL DEFAULT 0,
    tasks_total          INT NOT NULL DEFAULT 0,
    tasks_completed      INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ NULL,
    deleted_by      UUID        NULL
);
```

**Índices:**
```sql
CREATE UNIQUE INDEX uq_crs_scores_employee_week
    ON crs_scores (employee_id, week_start)
    WHERE deleted_at IS NULL;

CREATE INDEX idx_crs_scores_organization_id ON crs_scores (organization_id);
CREATE INDEX idx_crs_scores_employee_id ON crs_scores (employee_id);
CREATE INDEX idx_crs_scores_checkout_id ON crs_scores (checkout_id);
CREATE INDEX idx_crs_scores_week_start ON crs_scores (week_start);
```

---

## Migración Alembic

Archivo: `apps/backend/src/shared/database/migrations/202507051200_create_check_outs_crs_scores.py`

- `upgrade()` — crear tablas: `check_outs` → `crs_scores`
- `downgrade()` — eliminar: `crs_scores` → `check_outs`

Revisión: `202507051200`
Down revision: `202506231200` (migración de projects/checkins/priorities/tasks)

---

## Decisiones de Diseño

| Decisión | Justificación |
|---|---|
| `checkin_id` FK en `check_outs` | Vincula directamente el checkout con su checkin (invariante de dominio) |
| Partial unique index `uq_check_outs_employee_week` | BR-002 + soft-delete compatible |
| `crs_scores` con `checkout_id` FK | Trazabilidad directa del cálculo al checkout que lo disparó |
| `formula_version` en `crs_scores` | Permite evolución de la fórmula sin perder historia (BR-011) |
| Campos `priorities_total/completed`, `tasks_total/completed` | Snapshot de los datos usados para el cálculo (auditoría BR-011) |
| `week_start` (no `week_period`) | Consistencia con tablas existentes |

---

## Criterios de Aceptación

- [ ] Tabla `check_outs` creada con todos los campos y constraints
- [ ] Tabla `crs_scores` creada con todos los campos y constraints
- [ ] `organization_id` con FK en ambas tablas
- [ ] Columnas de auditoría en ambas tablas
- [ ] Partial unique index `uq_check_outs_employee_week` (BR-002)
- [ ] Partial unique index `uq_crs_scores_employee_week`
- [ ] Todos los índices FK creados
- [ ] CHECK constraints para enums (`status`, `trend`, `risk_level`)
- [ ] Migración `upgrade()` ejecuta sin errores
- [ ] Migración `downgrade()` revierte completamente
- [ ] Re-ejecutar `upgrade()` después de `downgrade()` funciona

---

## Git Branch

`feature/003-weekly-checkout`
