# ER Model (Deep Dive)

## Jerarquía Principal

Organization 1:N Team
Team 1:N User

Project 1:N ProjectPhase
ProjectPhase 1:N Priority
Priority 1:N Task

User 1:N WeeklyCheckIn
User 1:N WeeklyCheckOut
User 1:N CRSScore

## Cardinalidades

Project (1) ---- (N) ProjectPhase
ProjectPhase (1) ---- (N) Priority
Priority (1) ---- (N) Task

## Ownership

Project Aggregate:
- projects
- project_phases

Priority Aggregate:
- priorities
- tasks
