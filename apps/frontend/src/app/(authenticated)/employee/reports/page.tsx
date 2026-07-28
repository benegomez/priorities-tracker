"use client";

import { useIndividualReport } from "@/features/reports/hooks/useIndividualReport";
import { ReportStatCard } from "@/features/reports/components/ReportStatCard";
import { ReportWeeklyBreakdown } from "@/features/reports/components/ReportWeeklyBreakdown";

export default function EmployeeReportsPage() {
  const { data, isLoading } = useIndividualReport(8);

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
      <h1 className="text-xl font-semibold text-gray-900">Mi Reporte</h1>

      <div className="grid grid-cols-3 gap-4">
        <ReportStatCard label="Total prioridades" value={data.total_priorities} sublabel={`Últimas ${data.period_weeks} semanas`} />
        <ReportStatCard label="Completadas" value={data.completed_priorities} />
        <ReportStatCard label="Tasa de cumplimiento" value={`${data.completion_rate.toFixed(1)}%`} sublabel={data.crs_trend ?? undefined} />
      </div>

      <div className="rounded-lg border border-border bg-white p-5">
        <h2 className="mb-4 text-sm font-medium text-gray-700">Desglose semanal</h2>
        <ReportWeeklyBreakdown rows={data.weekly_breakdown} />
      </div>
    </div>
  );
}
