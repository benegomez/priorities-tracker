# Constraints

## Foreign Keys

project_phases.project_id -> projects.id
priorities.phase_id -> project_phases.id
tasks.priority_id -> priorities.id

## Unique

users.organization_id + email

weekly_checkins.employee_id + week_period

weekly_checkouts.employee_id + week_period

## Check Constraints

crs_scores.score >= 0

crs_scores.score <= 100
