"use client";

import { useTeamReport } from "@/features/reports/hooks/useTeamReport";
import { ReportStatCard } from "@/features/reports/components/ReportStatCard";

export default function ManagerReportsPage() {
  const { data, isLoading } = useTeamReport(8);

  if (isLoading) {
    return (
      <div className="space-y-4 p-6" aria-label="Cargando reporte">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-20 animate-pulse rounded-lg bg-gray-100" />
        ))}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-xl font-semibold text-gray-900">Reporte del Equipo</h1>

      <div className="grid grid-cols-3 gap-4">
        <ReportStatCard label="Miembros" value={data.team_size} sublabel={`Últimas ${data.period_weeks} semanas`} />
        <ReportStatCard label="Cumplimiento promedio" value={`${data.avg_completion_rate.toFixed(1)}%`} />
        <ReportStatCard label="CRS promedio" value={data.avg_crs != null ? data.avg_crs.toFixed(1) : "—"} />
      </div>

      {data.members.length === 0 ? (
        <p className="py-8 text-center text-sm text-secondary">Sin miembros en el equipo.</p>
      ) : (
        <div className="rounded-lg border border-border bg-white">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-left text-secondary">
                <th className="px-4 py-3 font-medium">Miembro</th>
                <th className="px-4 py-3 font-medium">Cumplimiento</th>
                <th className="px-4 py-3 font-medium">CRS</th>
                <th className="px-4 py-3 font-medium">Tendencia</th>
              </tr>
            </thead>
            <tbody>
              {data.members.map((m) => (
                <tr key={m.id} className="border-b border-border last:border-0">
                  <td className="px-4 py-3">{m.first_name} {m.last_name}</td>
                  <td className="px-4 py-3">{m.completion_rate.toFixed(1)}%</td>
                  <td className="px-4 py-3">{m.crs != null ? m.crs.toFixed(1) : "—"}</td>
                  <td className="px-4 py-3">{m.trend ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
