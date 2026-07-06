"use client";

import { useMyTeam } from "@/features/teams/hooks/useMyTeam";
import { TeamTable } from "@/features/teams/components/TeamTable";
import { TeamEmptyState } from "@/features/teams/components/TeamEmptyState";
import { Skeleton } from "@/components/ui/skeleton";

export default function ManagerTeamPage() {
  const { data, isLoading, error } = useMyTeam();

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-gray-900">Mi Equipo</h1>
        <Skeleton className="h-64 w-full rounded-lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-gray-900">Mi Equipo</h1>
        <p className="text-danger">Error al cargar el equipo.</p>
      </div>
    );
  }

  const members = data?.members ?? [];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Mi Equipo</h1>
      {members.length === 0 ? <TeamEmptyState /> : <TeamTable members={members} />}
    </div>
  );
}
