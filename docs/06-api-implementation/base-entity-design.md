# Base Entity Design

BaseEntity
  ↓
AuditEntity
  ↓
OrganizationScopedEntity

## BaseEntity
- id UUID

## AuditEntity
- created_at
- updated_at
- created_by
- updated_by
- deleted_at
- deleted_by

## OrganizationScopedEntity
- organization_id
