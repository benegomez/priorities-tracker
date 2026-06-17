---
description: Gestiona el flujo Git del proyecto (branch, commit, push, PR) siguiendo Trunk-Based Development según ADR-001 y ADR-002.
---

Por favor ejecuta la operación git: $ARGUMENTS

## Operaciones Disponibles

| Comando | Descripción |
|---|---|
| `start <feature-name>` | Crear branch de feature desde main |
| `commit <mensaje>` | Commit con formato convencional |
| `push` | Push del branch actual |
| `pr <titulo>` | Preparar descripción del PR |
| `status` | Mostrar estado del branch y cambios pendientes |
| `hotfix <nombre>` | Crear branch de hotfix desde main |

---

## `start <feature-name>`

```bash
git checkout main
git pull origin main
git checkout -b feature/<feature-name>
```

Naming de branches:
- Feature: `feature/<kebab-case-description>` — ej. `feature/checkin-flow`
- Hotfix: `hotfix/<descripcion>` — ej. `hotfix/auth-token-expiry`
- Release: `release/v<MAJOR>.<MINOR>.<PATCH>` — ej. `release/v1.0.0`

---

## `commit <mensaje>`

Formato convencional obligatorio:
```
<type>(<scope>): <descripción en inglés, imperativo, minúsculas>
```

Tipos válidos:
| Tipo | Cuándo usarlo |
|---|---|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `refactor` | Refactoring sin cambio funcional |
| `test` | Agregar o modificar tests |
| `docs` | Solo documentación |
| `chore` | Tareas de build, deps, config |
| `perf` | Mejora de performance |

Scopes válidos (módulos del proyecto):
`auth`, `users`, `teams`, `projects`, `priorities`, `checkin`, `checkout`, `crs`, `reporting`, `ai`, `shared`, `db`, `frontend`, `infra`

Ejemplos:
```bash
git commit -m "feat(checkin): add create check-in use case"
git commit -m "fix(crs): correct priority weight calculation"
git commit -m "test(auth): add token expiry integration test"
git commit -m "docs(api): update checkin contract OpenAPI spec"
```

---

## `push`

```bash
git push origin $(git branch --show-current)
```

Si es el primer push del branch:
```bash
git push -u origin $(git branch --show-current)
```

---

## `pr <titulo>`

Genera la descripción del PR con esta estructura:

```markdown
## Resumen
<qué cambia y por qué — 2-3 líneas>

## Tipo de Cambio
- [ ] feat — nueva funcionalidad
- [ ] fix — corrección de bug
- [ ] refactor — sin cambio funcional
- [ ] docs — solo documentación

## ADR de Referencia
<ADR-XXX si aplica, o "N/A">

## Nivel de Riesgo
- [ ] Low — docs, refactoring menor
- [ ] Medium — nuevas APIs, cambios de UI
- [ ] High — cambios de schema, integraciones
- [ ] Critical — auth, CRS, planning cycle

## Checklist
- [ ] Tests pasan localmente
- [ ] Linting sin errores (ruff / eslint)
- [ ] Type check sin errores (mypy / tsc)
- [ ] Documentación actualizada (si aplica)
- [ ] Sin secretos ni credenciales en el código
- [ ] Migración Alembic incluida (si hay cambios de schema)

## Validación
<cómo se validó el cambio — curl, tests, navegador>
```

Luego abrir el PR en GitHub apuntando a `main`.

---

## `status`

```bash
git status
git log main..HEAD --oneline
git diff --stat main
```

Muestra: branch actual, commits pendientes de merge, y archivos modificados.

---

## Reglas Obligatorias

- Commits directos a `main` están **prohibidos** — siempre mediante PR
- Nunca hacer `git push --force` en `main`
- Un PR por feature — no acumular múltiples features en un branch
- El merge solo ocurre después de que el usuario valide localmente y el pipeline de GitHub Actions esté verde
