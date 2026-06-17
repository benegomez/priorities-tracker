# Entities (Deep Dive)

## Organization
Atributos:
- id
- name
- status

## User
- id
- organization_id
- manager_id
- role
- status

## Project
- id
- organization_id
- name
- description
- status

Validaciones:
- nombre obligatorio
- organization_id obligatorio

## ProjectPhase
- id
- project_id
- name
- status

## Priority
- id
- phase_id
- owner_id
- week_period
- title
- description
- status

Validaciones:
- phase_id obligatorio
- owner_id obligatorio

## Task
- id
- priority_id
- title
- status

## WeeklyCheckIn
- id
- employee_id
- week_period
- status

## WeeklyCheckOut
- id
- employee_id
- week_period
- status

## CommitmentReliabilityScore
- employee_id
- week_period
- score
- trend
- risk_level
