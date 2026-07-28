"use client";

import { use } from "react";
import { useProjectReport } from "@/features/reports/hooks/useProjectReport";
import { ReportStatCard } from "@/features/reports/components/ReportStatCard";

export default function ProjectReportPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { data, isLoading } = useProjectReport(id, 8);

  if (isLoading) {
    return (
      <div className="space-y-4 p-6" aria-label="Cargando reporte">
        {[1, 2].map((i) => (
          <div key={i} className="h-20 animate-pulse rounded-lg bg-gray-100" />
        ))}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-xl font-semibold text-gray-900">{data.project.name}</h1>

      <div className="grid grid-cols-3 gap-4">
        <ReportStatCard label="Total prioridades" value={data.total_priorities} sublabel={`Últimas ${data.period_weeks} semanas`} />
        <ReportStatCard label="Completadas" value={data.completed_priorities} />
        <ReportStatCard label="Tasa de cumplimiento" value={`${data.completion_rate.toFixed(1)}%`} />
      </div>

      <div className="rounded-lg border border-border bg-white">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left text-secondary">
              <th className="px-4 py-3 font-medium">Fase</th>
              <th className="px-4 py-3 font-medium">Prioridades</th>
              <th className="px-4 py-3 font-medium">Completadas</th>
              <th className="px-4 py-3 font-medium">Cumplimiento</th>
            </tr>
          </thead>
          <tbody>
            {data.phases.map((phase) => (
              <tr key={phase.id} className="border-b border-border last:border-0">
                <td className="px-4 py-3">{phase.name}</td>
                <td className="px-4 py-3">{phase.total_priorities}</td>
                <td className="px-4 py-3">{phase.completed_priorities}</td>
                <td className="px-4 py-3">{phase.completion_rate.toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
