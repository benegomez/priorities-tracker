
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    team_id UUID NULL REFERENCES teams(id),
    manager_id UUID NULL REFERENCES users(id),
    email VARCHAR(320) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_users_org_email UNIQUE (organization_id,email)
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE project_phases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE priorities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    phase_id UUID NOT NULL REFERENCES project_phases(id),
    owner_id UUID NOT NULL REFERENCES users(id),
    week_period DATE NOT NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    status VARCHAR(30) NOT NULL,
    carried_over_from_priority_id UUID NULL REFERENCES priorities(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    priority_id UUID NOT NULL REFERENCES priorities(id) ON DELETE CASCADE,
    title VARCHAR(300) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE weekly_checkins (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    employee_id UUID NOT NULL REFERENCES users(id),
    week_period DATE NOT NULL,
    status VARCHAR(30) NOT NULL,
    comments TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_checkin_employee_week UNIQUE(employee_id, week_period)
);

CREATE TABLE weekly_checkouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    employee_id UUID NOT NULL REFERENCES users(id),
    week_period DATE NOT NULL,
    status VARCHAR(30) NOT NULL,
    blockers TEXT,
    comments TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_checkout_employee_week UNIQUE(employee_id, week_period)
);

CREATE TABLE crs_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    employee_id UUID NOT NULL REFERENCES users(id),
    week_period DATE NOT NULL,
    score NUMERIC(5,2) NOT NULL CHECK (score >= 0 AND score <= 100),
    trend VARCHAR(20) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    algorithm_version VARCHAR(20) NOT NULL DEFAULT 'CRS-1.0',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    user_id UUID NULL REFERENCES users(id),
    event_type VARCHAR(100) NOT NULL,
    entity_name VARCHAR(100) NOT NULL,
    entity_id UUID,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_org ON users(organization_id);
CREATE INDEX idx_users_manager ON users(manager_id);
CREATE INDEX idx_projects_org ON projects(organization_id);
CREATE INDEX idx_priorities_owner_week ON priorities(owner_id, week_period);
CREATE INDEX idx_priorities_phase ON priorities(phase_id);
CREATE INDEX idx_crs_employee_week ON crs_scores(employee_id, week_period);
CREATE INDEX idx_audit_org_created ON audit_logs(organization_id, created_at);
