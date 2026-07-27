"use client";

import { Card, CardContent } from "@/components/ui/card";
import type { AdminTeamResponse } from "../services/team-service";

interface AdminTeamTableProps {
  teams: AdminTeamResponse[];
  total: number;
  page: number;
  pages: number;
  onPageChange: (p: number) => void;
  onEdit: (team: AdminTeamResponse) => void;
  onViewMembers: (team: AdminTeamResponse) => void;
}

export function AdminTeamTable({
  teams,
  total,
  page,
  pages,
  onPageChange,
  onEdit,
  onViewMembers,
}: AdminTeamTableProps) {
  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <span className="text-sm text-gray-500 self-center">{total} equipo(s)</span>
      </div>

      {teams.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-gray-500 text-sm">
            No hay equipos registrados.
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="p-0 overflow-x-auto">
            <table className="w-full text-sm" role="table">
              <thead>
                <tr className="border-b border-gray-100 bg-gray-50">
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Nombre</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Manager</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Miembros</th>
                  <th className="text-right px-4 py-3 font-medium text-gray-600">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {teams.map((team) => (
                  <tr key={team.id} className="border-b border-gray-50 hover:bg-gray-50/50">
                    <td className="px-4 py-3 font-medium">{team.name}</td>
                    <td className="px-4 py-3 text-gray-600">{team.manager_name ?? "—"}</td>
                    <td className="px-4 py-3 text-gray-600">{team.member_count}</td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-3">
                        <button
                          onClick={() => onEdit(team)}
                          className="text-xs text-primary hover:underline"
                          aria-label={`Editar ${team.name}`}
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => onViewMembers(team)}
                          className="text-xs text-gray-600 hover:underline"
                          aria-label={`Ver miembros de ${team.name}`}
                        >
                          Ver miembros
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>
      )}

      {pages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1}
            className="rounded px-3 py-1 text-sm border border-gray-300 disabled:opacity-40 hover:bg-gray-50"
          >
            ← Anterior
          </button>
          <span className="text-sm text-gray-600">
            Página {page} de {pages}
          </span>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= pages}
            className="rounded px-3 py-1 text-sm border border-gray-300 disabled:opacity-40 hover:bg-gray-50"
          >
            Siguiente →
          </button>
        </div>
      )}
    </div>
  );
}
