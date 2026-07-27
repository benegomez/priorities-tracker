"use client";

import { Card, CardContent } from "@/components/ui/card";
import type { UserResponse } from "../services/user-service";
import { UserStatusBadge } from "./UserStatusBadge";

const ROLE_LABELS: Record<string, string> = {
  administrator: "Administrador",
  manager: "Manager",
  employee: "Empleado",
};

interface UserTableProps {
  users: UserResponse[];
  total: number;
  page: number;
  pages: number;
  roleFilter: string;
  statusFilter: string;
  onRoleFilter: (v: string) => void;
  onStatusFilter: (v: string) => void;
  onPageChange: (p: number) => void;
  onEdit: (user: UserResponse) => void;
  onToggleStatus: (user: UserResponse) => void;
  isTogglingId: string | null;
}

export function UserTable({
  users,
  total,
  page,
  pages,
  roleFilter,
  statusFilter,
  onRoleFilter,
  onStatusFilter,
  onPageChange,
  onEdit,
  onToggleStatus,
  isTogglingId,
}: UserTableProps) {
  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex gap-3">
        <select
          value={roleFilter}
          onChange={(e) => onRoleFilter(e.target.value)}
          className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          aria-label="Filtrar por rol"
        >
          <option value="">Todos los roles</option>
          <option value="administrator">Administrador</option>
          <option value="manager">Manager</option>
          <option value="employee">Empleado</option>
        </select>
        <select
          value={statusFilter}
          onChange={(e) => onStatusFilter(e.target.value)}
          className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          aria-label="Filtrar por estado"
        >
          <option value="">Todos los estados</option>
          <option value="active">Activo</option>
          <option value="inactive">Inactivo</option>
        </select>
        <span className="ml-auto text-sm text-gray-500 self-center">{total} usuario(s)</span>
      </div>

      {/* Table */}
      {users.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-gray-500 text-sm">
            No hay usuarios que coincidan con los filtros.
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="p-0 overflow-x-auto">
            <table className="w-full text-sm" role="table">
              <thead>
                <tr className="border-b border-gray-100 bg-gray-50">
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Nombre</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Email</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Rol</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Estado</th>
                  <th className="text-left px-4 py-3 font-medium text-gray-600">Manager</th>
                  <th className="text-right px-4 py-3 font-medium text-gray-600">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id} className="border-b border-gray-50 hover:bg-gray-50/50">
                    <td className="px-4 py-3 font-medium">
                      {user.first_name} {user.last_name}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{user.email}</td>
                    <td className="px-4 py-3 text-gray-600">{ROLE_LABELS[user.role] ?? user.role}</td>
                    <td className="px-4 py-3">
                      <UserStatusBadge status={user.status} />
                    </td>
                    <td className="px-4 py-3 text-gray-500">{user.manager_name ?? "—"}</td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => onEdit(user)}
                          className="text-xs text-primary hover:underline"
                          aria-label={`Editar ${user.first_name}`}
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => onToggleStatus(user)}
                          disabled={isTogglingId === user.id}
                          className={`text-xs hover:underline disabled:opacity-50 ${
                            user.status === "active" ? "text-red-500" : "text-green-600"
                          }`}
                          aria-label={user.status === "active" ? `Desactivar ${user.first_name}` : `Activar ${user.first_name}`}
                        >
                          {isTogglingId === user.id
                            ? "..."
                            : user.status === "active"
                            ? "Desactivar"
                            : "Activar"}
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

      {/* Pagination */}
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
