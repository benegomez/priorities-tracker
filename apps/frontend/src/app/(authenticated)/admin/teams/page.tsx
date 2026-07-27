"use client";

import { useState } from "react";
import type { ApiError } from "@/lib/api-client";
import type { AdminTeamResponse } from "@/features/teams/services/team-service";
import {
  useAdminTeams,
  useAddMember,
  useCreateTeam,
  useRemoveMember,
  useTeamDetail,
  useUpdateTeam,
} from "@/features/teams/hooks/useAdminTeams";
import { AdminTeamTable } from "@/features/teams/components/AdminTeamTable";
import { TeamFormModal } from "@/features/teams/components/TeamFormModal";
import { TeamMembersModal } from "@/features/teams/components/TeamMembersModal";
import { useUsers } from "@/features/users/hooks/useUsers";

export default function AdminTeamsPage() {
  const [page, setPage] = useState(1);
  const [showCreate, setShowCreate] = useState(false);
  const [editingTeam, setEditingTeam] = useState<AdminTeamResponse | null>(null);
  const [membersTeamId, setMembersTeamId] = useState<string | null>(null);
  const [formError, setFormError] = useState("");
  const [removingId, setRemovingId] = useState<string | null>(null);

  const { data, isLoading } = useAdminTeams({ page });
  const { data: teamDetail } = useTeamDetail(membersTeamId);
  const { data: usersData } = useUsers();

  const managers =
    usersData?.items.filter((u) => u.role === "manager" || u.role === "administrator") ?? [];
  const allUsers = usersData?.items ?? [];

  const createMutation = useCreateTeam();
  const updateMutation = useUpdateTeam();
  const addMemberMutation = useAddMember();
  const removeMemberMutation = useRemoveMember();

  function handleCreate(formData: unknown) {
    setFormError("");
    createMutation.mutate(formData as Parameters<typeof createMutation.mutate>[0], {
      onSuccess: () => setShowCreate(false),
      onError: (err) => {
        const apiErr = err as unknown as ApiError;
        setFormError(apiErr.message ?? "Error al crear el equipo");
      },
    });
  }

  function handleEdit(formData: unknown) {
    if (!editingTeam) return;
    setFormError("");
    updateMutation.mutate(
      { id: editingTeam.id, data: formData as Parameters<typeof updateMutation.mutate>[0]["data"] },
      {
        onSuccess: () => setEditingTeam(null),
        onError: (err) => {
          const apiErr = err as unknown as ApiError;
          setFormError(apiErr.message ?? "Error al actualizar el equipo");
        },
      }
    );
  }

  function handleAddMember(userId: string) {
    if (!membersTeamId) return;
    addMemberMutation.mutate({ teamId: membersTeamId, userId });
  }

  function handleRemoveMember(userId: string) {
    if (!membersTeamId) return;
    setRemovingId(userId);
    removeMemberMutation.mutate(
      { teamId: membersTeamId, userId },
      { onSettled: () => setRemovingId(null) }
    );
  }

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Gestión de Equipos</h1>
        <button
          onClick={() => { setShowCreate(true); setFormError(""); }}
          className="rounded-lg bg-primary px-4 py-2 text-sm text-white hover:bg-primary/90"
        >
          + Nuevo Equipo
        </button>
      </header>

      {isLoading ? (
        <div className="space-y-3 animate-pulse">
          <div className="h-8 w-64 bg-gray-200 rounded" />
          <div className="h-48 bg-gray-200 rounded-lg" />
        </div>
      ) : (
        <AdminTeamTable
          teams={data?.items ?? []}
          total={data?.total ?? 0}
          page={data?.page ?? 1}
          pages={data?.pages ?? 1}
          onPageChange={setPage}
          onEdit={(team) => { setEditingTeam(team); setFormError(""); }}
          onViewMembers={(team) => setMembersTeamId(team.id)}
        />
      )}

      {showCreate && (
        <TeamFormModal
          mode="create"
          managers={managers}
          onSubmit={handleCreate}
          onClose={() => setShowCreate(false)}
          isPending={createMutation.isPending}
          error={formError}
        />
      )}

      {editingTeam && (
        <TeamFormModal
          mode="edit"
          team={editingTeam}
          managers={managers}
          onSubmit={handleEdit}
          onClose={() => setEditingTeam(null)}
          isPending={updateMutation.isPending}
          error={formError}
        />
      )}

      {membersTeamId && teamDetail && (
        <TeamMembersModal
          team={teamDetail}
          allUsers={allUsers}
          onAddMember={handleAddMember}
          onRemoveMember={handleRemoveMember}
          onClose={() => setMembersTeamId(null)}
          isAddPending={addMemberMutation.isPending}
          isRemovingId={removingId}
        />
      )}
    </div>
  );
}
