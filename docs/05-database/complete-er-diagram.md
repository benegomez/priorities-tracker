# Complete ER Diagram

```text
Organization
 ├─ Teams
 │   └─ Users
 ├─ Projects
 │   └─ ProjectPhases
 │       └─ Priorities
 │           └─ Tasks
 ├─ WeeklyCheckIns
 ├─ WeeklyCheckOuts
 └─ CRS Scores
```

## Cardinalidades
- Organization 1:N Teams
- Team 1:N Users
- Project 1:N ProjectPhase
- ProjectPhase 1:N Priority
- Priority 1:N Task
- User 1:N CheckIns
- User 1:N CheckOuts
- User 1:N CRS Scores
