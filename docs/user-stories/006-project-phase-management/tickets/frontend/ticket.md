---
status: done
type: frontend
story: docs/user-stories/006-project-phase-management/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Medium
complexity: L
---

# [FE] US-006 — Project & Phase Management UI

## Objetivo

Implementar las páginas de gestión de proyectos (lista + detalle con fases y miembros) y reemplazar el `MOCK_PHASES` del PriorityForm con datos reales del endpoint `GET /projects/phases/available`.

## Scope

2 páginas nuevas (lista + detalle), refactor PriorityForm, nuevos hooks y servicios.

## Dependencia

Ticket BE completado — endpoints disponibles.

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  app/(authenticated)/admin/projects/
    page.tsx                              - CREATE (lista de proyectos)
  app/(authenticated)/admin/projects/[id]/
    page.tsx                              - CREATE (detalle proyecto)
  app/(authenticated)/manager/projects/
    page.tsx                              - CREATE (misma vista que admin)

  features/projects/
    services/
      project-service.ts                  - CREATE (API client)
    schemas/
      project-schema.ts                   - CREATE (Zod)
    hooks/
      useProjects.ts                      - CREATE (useQuery lista)
      useProjectDetail.ts                 - CREATE (useQuery detalle)
      useCreateProject.ts                 - CREATE (useMutation)
      useUpdateProject.ts                 - CREATE (useMutation)
      useCreatePhase.ts                   - CREATE (useMutation)
      useUpdatePhase.ts                   - CREATE (useMutation)
      useAddMember.ts                     - CREATE (useMutation)
      useRemoveMember.ts                  - CREATE (useMutation)
      useAvailablePhases.ts               - CREATE (useQuery para PriorityForm)
    components/
      ProjectList.tsx                     - CREATE (lista de cards)
      ProjectCard.tsx                     - CREATE (card en la lista)
      ProjectDetail.tsx                   - CREATE (vista detalle)
      ProjectForm.tsx                     - CREATE (crear/editar proyecto)
      PhaseList.tsx                       - CREATE (lista de fases inline)
      PhaseForm.tsx                       - CREATE (crear/editar fase)
      PhaseStatusSelect.tsx               - CREATE (cambio de estado)
      MemberList.tsx                      - CREATE (lista de participantes)
      MemberAddForm.tsx                   - CREATE (agregar miembro)
      ProjectStatusBar.tsx                - CREATE (barra de estado con transiciones)

  features/priorities/components/
    PriorityForm.tsx                      - MODIFY (usar useAvailablePhases en vez de MOCK_PHASES)

  app/(authenticated)/employee/checkin/
    page.tsx                              - MODIFY (remover MOCK_PHASES)

  config/navigation.ts                    - MODIFY (agregar "Proyectos" a admin y manager nav)
```

---

## Flujo de UI

### Lista de Proyectos (`/admin/projects` o `/manager/projects`)

- Header con título + botón "Nuevo Proyecto"
- Lista de ProjectCards con: nombre, estado (badge), owner, conteo fases/miembros
- Click en card → navega a detalle
- Filtro por estado (opcional)

### Detalle del Proyecto (`/admin/projects/[id]`)

- Header: nombre + badge estado + botón editar
- Descripción + responsable
- Sección "Fases": lista inline con botón agregar + editar nombre/estado
- Sección "Participantes": lista con botón agregar + remover
- Sección "Estado": barra visual con transiciones válidas

### Selección de Owner y Participantes

- **Hook `useOrgMembers()`**: consume `GET /api/v1/users/org-members` para obtener lista de usuarios activos de la org
- **Owner (responsable)**: Select dropdown con búsqueda que muestra nombre + rol de cada usuario. Cualquier usuario puede ser owner.
- **Agregar participante**: Select dropdown que muestra usuarios de la org que NO son ya miembros del proyecto. Al seleccionar, se agrega inmediatamente.
- Ambos selects muestran: `Nombre Completo (rol)` como label de cada opción

### PriorityForm (refactor)

- Reemplazar `MOCK_PHASES` por `useAvailablePhases()` hook
- El hook llama a `GET /projects/phases/available`
- Select muestra "Proyecto → Fase" como antes, pero con datos reales

---

## Archivos Adicionales

```
apps/frontend/src/
  features/projects/
    hooks/
      useOrgMembers.ts                    - CREATE (useQuery para lista de usuarios de la org)
    components/
      UserSelect.tsx                      - CREATE (select dropdown con búsqueda para elegir usuario)
```

---

## Resolución TD-007

Al completar esta US:
1. Eliminar `MOCK_PHASES` de `page.tsx`
2. `PriorityForm` recibe fases de `useAvailablePhases()` hook
3. TD-007 se marca como `closed`

---

## Tests Requeridos

### Component Tests

- [ ] `test_ProjectList_renders_project_cards`
- [ ] `test_ProjectCard_shows_name_status_owner`
- [ ] `test_ProjectForm_validates_required_fields`
- [ ] `test_ProjectForm_shows_owner_select_with_users`
- [ ] `test_ProjectForm_submits_with_valid_data`
- [ ] `test_PhaseList_renders_phases_with_status`
- [ ] `test_PhaseForm_validates_name_required`
- [ ] `test_MemberList_renders_members`
- [ ] `test_MemberAddForm_shows_user_select`
- [ ] `test_MemberAddForm_filters_existing_members`
- [ ] `test_UserSelect_renders_users_with_name_and_role`
- [ ] `test_ProjectStatusBar_shows_valid_transitions`
- [ ] `test_PriorityForm_uses_available_phases_hook`
- [ ] `test_available_phases_hook_fetches_from_api`

### Schema Tests

- [ ] `test_project_schema_validates_name_required`
- [ ] `test_phase_schema_validates_name_required`

---

## Accesibilidad

- [ ] Formularios con labels
- [ ] Badges de estado con aria-label
- [ ] Botones de acción con aria-label descriptivo
- [ ] Tablas/listas navegables por teclado

---

## Criterios de Aceptación

- [ ] Lista de proyectos muestra todos los proyectos de la organización
- [ ] Se puede crear un proyecto con nombre, descripción y responsable (select de usuarios)
- [ ] Owner se selecciona de un dropdown con usuarios de la org (nombre + rol)
- [ ] Detalle muestra fases y participantes
- [ ] Se puede agregar/editar fases inline
- [ ] Se puede cambiar estado del proyecto (state machine)
- [ ] Se puede agregar participantes desde un select de usuarios (filtra ya miembros)
- [ ] Se puede remover participantes
- [ ] PriorityForm usa datos reales (no MOCK_PHASES)
- [ ] Solo admin/manager ven la sección de proyectos
- [ ] Responsive: funciona en mobile
- [ ] TD-007 cerrado

---

## Git Branch

`feature/006-project-phase-management`
