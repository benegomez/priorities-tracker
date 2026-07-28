"use client";

import { useRouter } from "next/navigation";
import { useTeamReport } from "@/features/reports/hooks/useTeamReport";
import { ReportStatCard } from "@/features/reports/components/ReportStatCard";
import { TeamCRSBadge } from "@/features/teams/components/TeamCRSBadge";
import { CRSTrendIndicator } from "@/features/crs/components/CRSTrendIndicator";
import { TeamEmptyState } from "@/features/teams/components/TeamEmptyState";
import type { TeamMemberSummary } from "@/features/reports/services/report-service";

function getRiskLevel(crs: number | null): "low" | "moderate" | "high" {
  if (crs === null) return "high";
  if (crs >= 75) return "low";
  if (crs >= 60) return "moderate";
  return "high";
}

function sortByRisk(members: TeamMemberSummary[]): TeamMemberSummary[] {
  return [...members].sort((a, b) => {
    if (a.crs === null && b.crs === null) return 0;
    if (a.crs === null) return -1;
    if (b.crs === null) return 1;
    return a.crs - b.crs;
  });
}

export default function ManagerTeamCRSPage() {
  const router = useRouter();
  const { data, isLoading } = useTeamReport(8);

  if (isLoading) {
    return (
      <div className="space-y-4 p-6" aria-label="Cargando CRS del equipo">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-20 animate-pulse rounded-lg bg-gray-100" />
        ))}
      </div>
    );
  }

  if (!data || data.members.length === 0) {
    return (
      <div className="p-6 space-y-4">
        <h1 className="text-xl font-semibold text-gray-900">CRS del Equipo</h1>
        <TeamEmptyState />
      </div>
    );
  }

  const atRisk = data.members.filter((m) => m.crs === null || m.crs < 60).length;
  const sorted = sortByRisk(data.members);

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-xl font-semibold text-gray-900">CRS del Equipo</h1>

      <div className="grid grid-cols-3 gap-4">
        <ReportStatCard
          label="CRS Promedio"
          value={data.avg_crs != null ? data.avg_crs.toFixed(1) : "—"}
          sublabel="Últimas 8 semanas"
        />
        <ReportStatCard
          label="En Riesgo Alto"
          value={atRisk}
          sublabel="CRS < 60 o sin datos"
        />
        <ReportStatCard
          label="Total Miembros"
          value={data.team_size}
        />
      </div>

      <div className="rounded-lg border border-border bg-white">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left text-secondary">
              <th className="px-4 py-3 font-medium">Miembro</th>
              <th className="px-4 py-3 font-medium">CRS</th>
              <th className="px-4 py-3 font-medium">Tendencia</th>
              <th className="px-4 py-3 font-medium">Cumplimiento</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((member) => (
              <tr
                key={member.id}
                className="border-b border-border last:border-0 cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => router.push(`/manager/team/${member.id}`)}
              >
                <td className="px-4 py-3 font-medium text-gray-900">
                  {member.first_name} {member.last_name}
                </td>
                <td className="px-4 py-3">
                  {member.crs != null ? (
                    <TeamCRSBadge score={member.crs} riskLevel={getRiskLevel(member.crs)} />
                  ) : (
                    <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-500">
                      Sin datos
                    </span>
                  )}
                </td>
                <td className="px-4 py-3">
                  {member.trend ? (
                    <CRSTrendIndicator trend={member.trend as "improving" | "stable" | "declining"} />
                  ) : (
                    <span className="text-secondary">—</span>
                  )}
                </td>
                <td className="px-4 py-3 text-gray-700">
                  {member.completion_rate.toFixed(1)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
