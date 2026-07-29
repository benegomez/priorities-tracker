# Screenshots — Priorities Tracker

Esta carpeta contiene las capturas de pantalla referenciadas en el `README.md` (sección 1.3).

## Cómo agregar imágenes

1. Toma la captura de pantalla de la funcionalidad correspondiente
2. Guárdala con el nombre exacto indicado abajo (formato `.png` recomendado)
3. Colócala en esta carpeta (`docs/screenshots/`)
4. El README la mostrará automáticamente

## Archivos esperados

### Flujo 1 — Check-In Semanal
| Archivo | Descripción |
|---|---|
| `checkin-01-main.png` | Página `/employee/checkin` con estado de la semana actual |
| `checkin-02-priority-form.png` | Formulario de nueva prioridad con selector de proyecto/fase |
| `checkin-03-priorities-list.png` | Lista de PriorityCard con tareas expandidas |
| `checkin-04-submitted.png` | Estado "Enviado" con confirmación |

### Flujo 2 — Check-Out Semanal
| Archivo | Descripción |
|---|---|
| `checkout-01-main.png` | Página `/employee/checkout` con prioridades cargadas |
| `checkout-02-marking.png` | CheckOutPriorityCard con checkboxes de prioridad y tareas |
| `checkout-03-notes.png` | Sección de notas y lessons_learned |
| `checkout-04-summary.png` | CheckOutSummary con contadores y CRS de la semana |

### Flujo 3 — Reportes
| Archivo | Descripción |
|---|---|
| `reports-01-individual.png` | Página `/employee/reports` con ReportStatCard y breakdown semanal |
| `reports-02-team.png` | Página `/manager/reports` con stats del equipo y tabla de miembros |
| `reports-03-project.png` | Página `/manager/reports/project/[id]` con desglose por fases |

### Flujo 4 — Administración de Proyectos
| Archivo | Descripción |
|---|---|
| `admin-projects-01-list.png` | Página `/admin/projects` con tabla de proyectos |
| `admin-projects-02-create.png` | Modal de creación de proyecto |
| `admin-projects-03-detail.png` | Detalle de proyecto con fases y participantes |
| `admin-projects-04-status.png` | Selector de estado con transiciones válidas |

### Flujo 5 — Vista de Equipo del Manager
| Archivo | Descripción |
|---|---|
| `manager-team-01-overview.png` | Página `/manager/team` con tabla de miembros y CRS badges |
| `manager-team-02-individual.png` | Página `/manager/team/[id]` con CRS score e historial |
| `manager-team-03-history.png` | Tabla de historial interactiva con check-in de semana seleccionada |

## Formato recomendado

- Resolución: 1280×800 o superior
- Formato: PNG
- Navegador: Chrome o Firefox en modo claro
- Datos: usar las cuentas del seed demo (`manager@org-alpha.com / Manager1234!`)
