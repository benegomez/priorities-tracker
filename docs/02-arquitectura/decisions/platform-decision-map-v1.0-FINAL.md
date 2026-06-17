# PrioritiesTracker Platform Decision Map
Version: 1.0 FINAL

## Purpose

The Platform Decision Map provides a consolidated view of the major architecture, platform, technology, governance, infrastructure, API, and domain decisions that define the PrioritiesTracker Enterprise Architecture Baseline.

The objective is to provide a single navigation artifact linking principles, ADRs, governance assets, and implementation direction.

---

# Decision Hierarchy

Business Strategy
→ Architecture Principles
→ ADRs
→ Standards
→ Implementation

All platform decisions shall align with this hierarchy.

---

# Strategic Decisions

## SD-001

Decision:
Modular Monolith Platform

Source:
ADR-003

Status:
Approved

Impact:
Platform Architecture

---

## SD-002

Decision:
Domain-Driven Design

Source:
ADR-010

Status:
Approved

Impact:
Domain Architecture

---

## SD-003

Decision:
API First

Source:
ADR-008

Status:
Approved

Impact:
Integration Architecture

---

## SD-004

Decision:
OpenAPI Contract First

Source:
ADR-009

Status:
Approved

Impact:
API Governance

---

# Repository Decisions

## RD-001

Decision:
Monorepo Strategy

Source:
ADR-001

Status:
Approved

---

## RD-002

Decision:
Repository Governance Model

Source:
ADR-002

Status:
Approved

---

# Infrastructure Decisions

## ID-001

Decision:
Docker Compose First

Source:
ADR-004

Status:
Approved

---

## ID-002

Decision:
Kubernetes Deferred Until Justified

Source:
ADR-004

Status:
Approved

---

# Quality Decisions

## QD-001

Decision:
Risk-Based Testing

Source:
ADR-005

Status:
Approved

---

# Backend Decisions

## BD-001

Decision:
Python

Source:
ADR-006

Status:
Approved

---

## BD-002

Decision:
FastAPI

Source:
ADR-006

Status:
Approved

---

## BD-003

Decision:
PostgreSQL

Source:
ADR-006

Status:
Approved

---

## BD-004

Decision:
SQLAlchemy

Source:
ADR-006

Status:
Approved

---

# Frontend Decisions

## FD-001

Decision:
React

Source:
ADR-007

Status:
Approved

---

## FD-002

Decision:
Next.js

Source:
ADR-007

Status:
Approved

---

## FD-003

Decision:
TypeScript

Source:
ADR-007

Status:
Approved

---

# Governance Decisions

## GD-001

Decision:
Architecture Principles Govern Platform

Source:
architecture-principles.md

Status:
Approved

---

## GD-002

Decision:
Architecture Board Approval Required

Source:
governance-charter.md

Status:
Approved

---

## GD-003

Decision:
Technology Radar Controls Technology Adoption

Source:
technology-radar.md

Status:
Approved

---

# Domain Decisions

## DD-001

Decision:
Organization Context

Source:
ADR-010

Status:
Approved

---

## DD-002

Decision:
Commitment Context

Source:
ADR-010

Status:
Approved

---

## DD-003

Decision:
Execution Context

Source:
ADR-010

Status:
Approved

---

## DD-004

Decision:
Reliability Context

Source:
ADR-010

Status:
Approved

---

# Integration Decisions

## IN-001

Decision:
REST APIs

Source:
ADR-008

Status:
Approved

---

## IN-002

Decision:
OpenAPI 3.x

Source:
ADR-009

Status:
Approved

---

# Security Decisions

## SEC-001

Decision:
Security by Design

Source:
architecture-principles.md

Status:
Approved

---

## SEC-002

Decision:
Externalized Secrets

Source:
ADR-004

Status:
Approved

---

# Decision Dependency Map

ADR-003 Platform Strategy
│
├── ADR-004 Infrastructure
├── ADR-005 Testing
├── ADR-006 Backend
├── ADR-007 Frontend
├── ADR-008 API First
├── ADR-009 OpenAPI
└── ADR-010 DDD

---

# Governance Artifacts

Reference Documents:

- architecture-principles.md
- governance-charter.md
- technology-radar.md
- architecture-decision-tree.md
- architecture-consistency-review.md
- traceability-matrix.md
- bounded-context-map.md

---

# Review Process

Decision Review Triggers:

- New technology adoption
- New bounded context
- New platform capability
- Infrastructure change
- Governance exception

---

# Metrics

Targets:

- ADR Compliance >95%
- Technology Compliance >95%
- Architecture Compliance >95%
- Traceability Coverage 100%

---

# Approval

Architecture Board Approved
Effective Date: 2026-06-16

---

# Conclusion

The Platform Decision Map provides a consolidated architecture navigation model that links strategic decisions, ADRs, governance assets, and implementation standards into a single enterprise reference document.
