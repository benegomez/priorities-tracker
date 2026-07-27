"use client";

import { useState } from "react";
import { useMyTeam } from "@/features/teams/hooks/useMyTeam";
import { WeeklySummaryBar } from "@/features/teams/components/WeeklySummaryBar";
import { WeeklyMemberRow } from "@/features/teams/components/WeeklyMemberRow";
import { TeamEmptyState } from "@/features/teams/components/TeamEmptyState";
import { Skeleton } from "@/components/ui/skeleton";

export default function ManagerWeeklyPage() {
  const { data, isLoading, error } = useMyTeam();
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const members = data?.members ?? [];
  const checkins = members.filter((m) => !!m.week_status.checkin_status).length;
  const checkouts = members.filter((m) => !!m.week_status.checkout_status).length;

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-gray-900">Vista Semanal</h1>
        <Skeleton className="h-12 w-full rounded-lg" />
        <Skeleton className="h-64 w-full rounded-lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-gray-900">Vista Semanal</h1>
        <p className="text-danger">Error al cargar el equipo.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Vista Semanal</h1>

      {members.length === 0 ? (
        <TeamEmptyState />
      ) : (
        <>
          <WeeklySummaryBar total={members.length} checkins={checkins} checkouts={checkouts} />
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-left text-xs font-medium uppercase text-secondary">
                <tr>
                  <th scope="col" className="px-4 py-3">Nombre</th>
                  <th scope="col" className="px-4 py-3">CRS</th>
                  <th scope="col" className="px-4 py-3">Tendencia</th>
                  <th scope="col" className="px-4 py-3">Check-In</th>
                  <th scope="col" className="px-4 py-3">Check-Out</th>
                </tr>
              </thead>
              <tbody className="bg-white">
                {members.map((member) => (
                  <WeeklyMemberRow
                    key={member.id}
                    member={member}
                    isExpanded={expandedId === member.id}
                    onToggle={() => setExpandedId(expandedId === member.id ? null : member.id)}
                  />
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
