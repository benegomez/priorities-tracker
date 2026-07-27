---
status: pending
type: frontend
story: docs/user-stories/013-admin-team-management/UserStory.md
depends-on: tickets/backend/ticket.md
risk_level: Medium
complexity: M
---

# [FE] US-013 — Admin Team Management UI

## Objetivo

Implementar la página `/admin/teams` con gestión completa de equipos: listar, crear, editar, ver detalle con miembros, asignar y remover miembros.

## Scope

Feature module `features/teams/` — se agregan componentes y hooks de administración. Los componentes existentes de visibilidad manager (`TeamTable`, `TeamCRSBadge`, etc.) no se modifican.

---

## Archivos a Crear / Modificar

```
apps/frontend/src/
  features/teams/
    services/
      team-service.ts              # MODIFY — agregar tipos y funciones admin
    hooks/
      useAdminTeams.ts             # nuevos hooks de administración
    components/
      AdminTeamTable.tsx           # tabla de equipos con acciones
      TeamFormModal.tsx            # modal crear/editar equipo
      TeamMembersModal.tsx         # modal ver/gestionar miembros del equipo
  app/(authenticated)/admin/
    teams/
      page.tsx                     # página principal /admin/teams
  tests/
    team-management.test.tsx       # tests de componentes
```

---

## Tipos nuevos en team-service.ts

```typescript
export interface AdminTeamResponse {
  id: string;
  name: string;
  manager_id: string | null;
  manager_name: string | null;
  member_count: number;
  created_at: string;
  updated_at: string;
}

export interface AdminTeamDetailResponse extends AdminTeamResponse {
  members: Array<{
    id: string;
    first_name: string;
    last_name: string;
    role: string;
    status: string;
  }>;
}

export interface AdminTeamListResponse {
  items: AdminTeamResponse[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface TeamCreate {
  name: string;
  manager_id?: string;
}

export interface TeamUpdate {
  name?: string;
  manager_id?: string;
}
```

## Funciones nuevas en team-service.ts

```typescript
listTeams(params?)       → GET /api/v1/teams
createTeam(data)         → POST /api/v1/teams
getTeamDetail(id)        → GET /api/v1/teams/{id}
updateTeam(id, data)     → PATCH /api/v1/teams/{id}
addMember(teamId, userId)    → POST /api/v1/teams/{id}/members
removeMember(teamId, userId) → DELETE /api/v1/teams/{id}/members/{user_id}
```

---

## Hooks (useAdminTeams.ts)

```typescript
useAdminTeams(filters?)      // useQuery — lista paginada
useCreateTeam()              // useMutation → invalida ["admin-teams"]
useUpdateTeam()              // useMutation → invalida ["admin-teams"]
useTeamDetail(id)            // useQuery — detalle con miembros
useAddMember()               // useMutation → invalida ["admin-teams", id]
useRemoveMember()            // useMutation → invalida ["admin-teams", id]
```

---

## Componentes

### AdminTeamTable
- Tabla con columnas: Nombre, Manager, Miembros, Acciones
- Acciones por fila: Editar, Ver miembros
- Paginación
- Botón "Nuevo Equipo"

### TeamFormModal
- Modo `create` y `edit`
- Campos: Nombre (requerido), Manager (select de usuarios con rol manager/administrator, opcional)
- Validación: nombre no vacío

### TeamMembersModal
- Lista de miembros actuales del equipo con nombre, rol y estado
- Botón "Remover" por miembro
- Sección "Agregar miembro": select de usuarios sin equipo o de cualquier usuario de la org
- Botón "Agregar"

---

## Página /admin/teams

Flujo:
1. Carga lista de equipos con `useAdminTeams`
2. Botón "Nuevo Equipo" → abre `TeamFormModal` en modo create
3. Clic "Editar" en fila → abre `TeamFormModal` en modo edit
4. Clic "Ver miembros" en fila → abre `TeamMembersModal` con detalle del equipo
5. Dentro de `TeamMembersModal`: remover o agregar miembros

---

## Navegación

Agregar entrada en `config/navigation.ts` para admin:
```typescript
{ href: "/admin/teams", label: "Equipos", icon: "Users2" }
```

---

## Tests Requeridos (team-management.test.tsx)

- [ ] `AdminTeamTable renders team list`
- [ ] `AdminTeamTable shows member count`
- [ ] `TeamFormModal renders create mode`
- [ ] `TeamFormModal renders edit mode with existing data`
- [ ] `TeamFormModal calls onSubmit with correct data`
- [ ] `TeamMembersModal renders member list`
- [ ] `TeamMembersModal calls onRemove when remove clicked`

---

## Criterios de Aceptación

- [ ] `/admin/teams` muestra lista paginada de equipos
- [ ] Crear equipo desde modal → tabla se actualiza
- [ ] Editar equipo → cambios reflejados en tabla
- [ ] Ver miembros → lista correcta con opción de remover
- [ ] Agregar miembro → aparece en lista de miembros
- [ ] Remover miembro → desaparece de lista
- [ ] Navegación admin incluye enlace a Equipos
- [ ] Componentes existentes de teams (manager view) no se modifican
- [ ] Tests pasan
- [ ] Build exitoso

---

## Git Branch

`feature/013-admin-team-management`
