/create-user-story          → crea UserStory.md con [original]
        ↓
/enrich-us <story-id>       → agrega [enhanced] con todo el análisis
        ↓
/create-tickets <story-id>  → tickets DB + BE + FE
        ↓
/create-plan <story-id>     → plan.md con checkboxes
        ↓
/develop-plan <story-id>    → implementación




User Story básica
      ↓
/enrich-us          → US enriquecida con FR, BRs, complejidad, riesgo
      ↓
/create-tickets     → 3 tickets (DB, BE, FE) con contratos y criterios
      ↓
/create-plan        → 3 plan.md con checkboxes fase por fase
      ↓
/develop-plan db    → Migración Alembic implementada
/run-tests unit     → Verificar
/git-flow pr        → PR database
      ↓ merge
/develop-plan be    → Casos de uso + endpoints implementados
/run-tests all      → PR gate completo (si L o XL)
/git-flow pr        → PR backend
      ↓ merge
/develop-plan fe    → Componentes + hooks implementados
/run-tests frontend → Tests frontend
/git-flow pr        → PR frontend
      ↓ merge
/update-docs        → Documentación sincronizada




/create-user-story → /enrich-us → /create-tickets → /create-plan → /develop-plan → /run-tests → /git-flow → /update-docs