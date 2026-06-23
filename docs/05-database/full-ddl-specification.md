# Full DDL Specification

## Estándares
- UUID PK
- TIMESTAMPTZ
- Soft Delete
- Audit Columns

---

## Tabla organizations

```sql
CREATE TABLE organizations (
    id              UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255)  NOT NULL,
    code            VARCHAR(50)   NOT NULL,
    status          VARCHAR(20)   NOT NULL DEFAULT 'active',
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ   NULL,
    deleted_by      UUID          NULL,
    CONSTRAINT uq_organizations_code UNIQUE (code),
    CONSTRAINT ck_organizations_status CHECK (status IN ('active', 'inactive'))
);
```

---

## Tabla users

```sql
CREATE TABLE users (
    id              UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID          NOT NULL REFERENCES organizations(id),
    manager_id      UUID          NULL REFERENCES users(id),
    email           VARCHAR(255)  NOT NULL,
    hashed_password TEXT          NOT NULL,
    role            VARCHAR(20)   NOT NULL,
    status          VARCHAR(20)   NOT NULL DEFAULT 'active',
    first_name      VARCHAR(100)  NOT NULL,
    last_name       VARCHAR(100)  NOT NULL,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ   NULL,
    deleted_by      UUID          NULL,
    CONSTRAINT ck_users_role CHECK (role IN ('administrator', 'manager', 'employee')),
    CONSTRAINT ck_users_status CHECK (status IN ('active', 'inactive'))
);

CREATE UNIQUE INDEX uq_users_email ON users (email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_organization_id ON users (organization_id);
CREATE INDEX idx_users_status ON users (status);
```

---

## Tabla refresh_tokens

```sql
CREATE TABLE refresh_tokens (
    id          UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID          NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash  TEXT          NOT NULL,
    expires_at  TIMESTAMPTZ   NOT NULL,
    revoked_at  TIMESTAMPTZ   NULL,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_refresh_tokens_token_hash ON refresh_tokens (token_hash);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens (user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens (expires_at);
```

---

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
