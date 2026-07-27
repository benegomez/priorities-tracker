"use client";

import { useEffect, useState } from "react";
import type { AdminTeamDetailResponse } from "../services/team-service";
import type { UserResponse } from "@/features/users/services/user-service";

interface TeamMembersModalProps {
  team: AdminTeamDetailResponse;
  allUsers: UserResponse[];
  onAddMember: (userId: string) => void;
  onRemoveMember: (userId: string) => void;
  onClose: () => void;
  isAddPending: boolean;
  isRemovingId: string | null;
}

const ROLE_LABELS: Record<string, string> = {
  administrator: "Administrador",
  manager: "Manager",
  employee: "Empleado",
};

export function TeamMembersModal({
  team,
  allUsers,
  onAddMember,
  onRemoveMember,
  onClose,
  isAddPending,
  isRemovingId,
}: TeamMembersModalProps) {
  const [selectedUserId, setSelectedUserId] = useState("");

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  const memberIds = new Set(team.members.map((m) => m.id));
  const availableUsers = allUsers.filter((u) => !memberIds.has(u.id) && u.status === "active");

  function handleAdd() {
    if (!selectedUserId) return;
    onAddMember(selectedUserId);
    setSelectedUserId("");
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      role="dialog"
      aria-modal="true"
      aria-label={`Miembros de ${team.name}`}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-white rounded-xl shadow-xl w-full max-w-lg p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Miembros — {team.name}</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-xl leading-none">
            ×
          </button>
        </div>

        {/* Member list */}
        <div className="space-y-1 max-h-60 overflow-y-auto">
          {team.members.length === 0 ? (
            <p className="text-sm text-gray-500 py-4 text-center">Sin miembros asignados.</p>
          ) : (
            team.members.map((member) => (
              <div
                key={member.id}
                className="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-gray-50"
              >
                <div>
                  <span className="text-sm font-medium">
                    {member.first_name} {member.last_name}
                  </span>
                  <span className="ml-2 text-xs text-gray-500">
                    {ROLE_LABELS[member.role] ?? member.role}
                  </span>
                </div>
                <button
                  onClick={() => onRemoveMember(member.id)}
                  disabled={isRemovingId === member.id}
                  className="text-xs text-red-500 hover:underline disabled:opacity-50"
                  aria-label={`Remover ${member.first_name}`}
                >
                  {isRemovingId === member.id ? "..." : "Remover"}
                </button>
              </div>
            ))
          )}
        </div>

        {/* Add member */}
        <div className="border-t pt-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Agregar miembro</p>
          <div className="flex gap-2">
            <select
              value={selectedUserId}
              onChange={(e) => setSelectedUserId(e.target.value)}
              className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              aria-label="Seleccionar usuario"
            >
              <option value="">Seleccionar usuario...</option>
              {availableUsers.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.first_name} {u.last_name} ({ROLE_LABELS[u.role] ?? u.role})
                </option>
              ))}
            </select>
            <button
              onClick={handleAdd}
              disabled={!selectedUserId || isAddPending}
              className="rounded-lg bg-primary px-4 py-2 text-sm text-white hover:bg-primary/90 disabled:opacity-50"
            >
              {isAddPending ? "..." : "Agregar"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
