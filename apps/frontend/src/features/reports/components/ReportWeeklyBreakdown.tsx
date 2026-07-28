import type { WeeklyBreakdownItem } from "../services/report-service";

interface ReportWeeklyBreakdownProps {
  rows: WeeklyBreakdownItem[];
}

export function ReportWeeklyBreakdown({ rows }: ReportWeeklyBreakdownProps) {
  if (rows.length === 0) {
    return (
      <p className="py-6 text-center text-sm text-secondary">Sin datos para el período seleccionado.</p>
    );
  }

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="border-b border-border text-left text-secondary">
          <th className="pb-2 font-medium">Semana</th>
          <th className="pb-2 font-medium">Comprometidas</th>
          <th className="pb-2 font-medium">Completadas</th>
          <th className="pb-2 font-medium">Arrastradas</th>
          <th className="pb-2 font-medium">CRS</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.week_start} className="border-b border-border last:border-0">
            <td className="py-2">{row.week_start}</td>
            <td className="py-2">{row.committed}</td>
            <td className="py-2">{row.completed}</td>
            <td className="py-2">{row.carried_over}</td>
            <td className="py-2">{row.crs != null ? row.crs.toFixed(1) : "—"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
