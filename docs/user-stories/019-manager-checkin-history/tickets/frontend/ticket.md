---
id: FE-019
us: 019-manager-checkin-history
layer: frontend
status: pending
risk: medium
---

# FE-019: Vista interactiva de historial + check-in por semana

## Objetivo

Hacer que la tabla de historial CRS en `/manager/team/[employeeId]` sea interactiva: al hacer clic en una fila se muestra el check-in de esa semana en la sección inferior.

## Archivos a modificar

| Archivo | Cambio |
|---|---|
| `features/teams/hooks/useTeamMemberCheckIn.ts` | Agregar param `weekStart?: string` |
| `features/teams/components/MemberCRSHistory.tsx` | Props `selectedWeek` + `onSelectWeek`, highlight de fila |
| `app/(authenticated)/manager/team/[employeeId]/page.tsx` | Estado `selectedWeek`, conectar componentes |

## Implementación

### Hook
```ts
// weekStart opcional → incluir en queryKey y URL
useTeamMemberCheckIn(employeeId, weekStart?)
queryKey: ["teams", "checkin", employeeId, weekStart ?? "current"]
url: weekStart ? `...?week_start=${weekStart}` : `...`
```

### MemberCRSHistory
```tsx
// Props nuevas
selectedWeek?: string
onSelectWeek?: (week: string) => void

// Fila seleccionada
className={item.week_start === selectedWeek ? "bg-primary/10 cursor-pointer" : "hover:bg-gray-50 cursor-pointer"}
onClick={() => onSelectWeek?.(item.week_start)}
```

### Página
```tsx
const [selectedWeek, setSelectedWeek] = useState<string | undefined>();
// Inicializar con la semana más reciente del historial CRS cuando cargue
// Pasar selectedWeek a useTeamMemberCheckIn
// Pasar selectedWeek y setSelectedWeek a MemberCRSHistory
// Título de sección: "Check-In — {selectedWeek ?? 'Semana actual'}"
```

## Acceptance Criteria

- [ ] Al cargar la página, la semana más reciente del historial está seleccionada
- [ ] Hacer clic en una fila resalta esa fila y carga el check-in correspondiente
- [ ] El título de la sección check-in refleja la semana seleccionada
- [ ] Si no hay check-in para la semana → mensaje informativo
- [ ] Loading skeleton mientras carga el check-in
- [ ] 4 tests pasando
