"use client";

import { useEffect, useState } from "react";
import type { UserResponse, UserCreate, UserUpdate } from "../services/user-service";

interface UserFormModalProps {
  mode: "create" | "edit";
  user?: UserResponse;
  managers: UserResponse[];
  onSubmit: (data: UserCreate | UserUpdate) => void;
  onClose: () => void;
  isPending: boolean;
  error?: string;
}

const ROLES = [
  { value: "employee", label: "Empleado" },
  { value: "manager", label: "Manager" },
  { value: "administrator", label: "Administrador" },
];

export function UserFormModal({
  mode,
  user,
  managers,
  onSubmit,
  onClose,
  isPending,
  error,
}: UserFormModalProps) {
  const [email, setEmail] = useState(user?.email ?? "");
  const [firstName, setFirstName] = useState(user?.first_name ?? "");
  const [lastName, setLastName] = useState(user?.last_name ?? "");
  const [role, setRole] = useState<string>(user?.role ?? "employee");
  const [managerId, setManagerId] = useState(user?.manager_id ?? "");
  const [newPassword, setNewPassword] = useState("");

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (mode === "create") {
      const data: UserCreate = {
        email,
        first_name: firstName,
        last_name: lastName,
        role,
        ...(managerId && { manager_id: managerId }),
      };
      onSubmit(data);
    } else {
      const data: UserUpdate = {
        first_name: firstName || undefined,
        last_name: lastName || undefined,
        role: role || undefined,
        ...(managerId && { manager_id: managerId }),
        ...(newPassword && { new_password: newPassword }),
      };
      onSubmit(data);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      role="dialog"
      aria-modal="true"
      aria-label={mode === "create" ? "Crear usuario" : "Editar usuario"}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6 space-y-4">
        <h2 className="text-lg font-semibold">
          {mode === "create" ? "Nuevo Usuario" : "Editar Usuario"}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-3">
          {mode === "create" && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="usuario@empresa.com"
              />
            </div>
          )}

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
              <input
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required={mode === "create"}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Apellido</label>
              <input
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required={mode === "create"}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Rol</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            >
              {ROLES.map((r) => (
                <option key={r.value} value={r.value}>{r.label}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Manager <span className="text-gray-400">(opcional)</span>
            </label>
            <select
              value={managerId}
              onChange={(e) => setManagerId(e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Sin manager asignado</option>
              {managers.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.first_name} {m.last_name}
                </option>
              ))}
            </select>
          </div>

          {mode === "edit" && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nueva contraseña <span className="text-gray-400">(dejar vacío para no cambiar)</span>
              </label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Mínimo 12 caracteres"
                autoComplete="new-password"
              />
            </div>
          )}

          {error && (
            <p className="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{error}</p>
          )}

          <div className="flex gap-2 pt-2">
            <button
              type="submit"
              disabled={isPending}
              className="flex-1 rounded-lg bg-primary px-4 py-2 text-sm text-white hover:bg-primary/90 disabled:opacity-50"
            >
              {isPending ? "Guardando..." : mode === "create" ? "Crear Usuario" : "Guardar Cambios"}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg border border-gray-300 px-4 py-2 text-sm hover:bg-gray-50"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
