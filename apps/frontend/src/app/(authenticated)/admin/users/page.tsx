"use client";

import { useState } from "react";
import type { ApiError } from "@/lib/api-client";
import type { UserCreatedResponse, UserResponse } from "@/features/users/services/user-service";
import { useCreateUser, useUpdateUser, useUpdateUserStatus, useUsers } from "@/features/users/hooks/useUsers";
import { TempPasswordModal } from "@/features/users/components/TempPasswordModal";
import { UserFormModal } from "@/features/users/components/UserFormModal";
import { UserTable } from "@/features/users/components/UserTable";

export default function AdminUsersPage() {
  const [page, setPage] = useState(1);
  const [roleFilter, setRoleFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  const [showCreate, setShowCreate] = useState(false);
  const [editingUser, setEditingUser] = useState<UserResponse | null>(null);
  const [tempPassword, setTempPassword] = useState<{ email: string; password: string } | null>(null);
  const [formError, setFormError] = useState("");
  const [togglingId, setTogglingId] = useState<string | null>(null);

  const { data, isLoading } = useUsers({
    page,
    role: roleFilter || undefined,
    status: statusFilter || undefined,
  });

  const managers = data?.items.filter((u) => u.role === "manager" || u.role === "administrator") ?? [];

  const createMutation = useCreateUser();
  const updateMutation = useUpdateUser();
  const statusMutation = useUpdateUserStatus();

  function handleCreate(formData: unknown) {
    setFormError("");
    createMutation.mutate(formData as Parameters<typeof createMutation.mutate>[0], {
      onSuccess: (result) => {
        const created = result as UserCreatedResponse;
        setShowCreate(false);
        setTempPassword({ email: created.email, password: created.temporary_password });
      },
      onError: (err) => {
        const apiErr = err as unknown as ApiError;
        setFormError(apiErr.message ?? "Error al crear el usuario");
      },
    });
  }

  function handleEdit(formData: unknown) {
    if (!editingUser) return;
    setFormError("");
    updateMutation.mutate(
      { id: editingUser.id, data: formData as Parameters<typeof updateMutation.mutate>[0]["data"] },
      {
        onSuccess: () => setEditingUser(null),
        onError: (err) => {
          const apiErr = err as unknown as ApiError;
          setFormError(apiErr.message ?? "Error al actualizar el usuario");
        },
      }
    );
  }

  function handleToggleStatus(user: UserResponse) {
    const newStatus = user.status === "active" ? "inactive" : "active";
    setTogglingId(user.id);
    statusMutation.mutate(
      { id: user.id, status: newStatus },
      {
        onSettled: () => setTogglingId(null),
        onError: (err) => {
          const apiErr = err as unknown as ApiError;
          alert(apiErr.message ?? "Error al cambiar el estado");
        },
      }
    );
  }

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Gestión de Usuarios</h1>
        <button
          onClick={() => { setShowCreate(true); setFormError(""); }}
          className="rounded-lg bg-primary px-4 py-2 text-sm text-white hover:bg-primary/90"
        >
          + Nuevo Usuario
        </button>
      </header>

      {isLoading ? (
        <div className="space-y-3 animate-pulse">
          <div className="h-8 w-64 bg-gray-200 rounded" />
          <div className="h-48 bg-gray-200 rounded-lg" />
        </div>
      ) : (
        <UserTable
          users={data?.items ?? []}
          total={data?.total ?? 0}
          page={data?.page ?? 1}
          pages={data?.pages ?? 1}
          roleFilter={roleFilter}
          statusFilter={statusFilter}
          onRoleFilter={(v) => { setRoleFilter(v); setPage(1); }}
          onStatusFilter={(v) => { setStatusFilter(v); setPage(1); }}
          onPageChange={setPage}
          onEdit={(user) => { setEditingUser(user); setFormError(""); }}
          onToggleStatus={handleToggleStatus}
          isTogglingId={togglingId}
        />
      )}

      {showCreate && (
        <UserFormModal
          mode="create"
          managers={managers}
          onSubmit={handleCreate}
          onClose={() => setShowCreate(false)}
          isPending={createMutation.isPending}
          error={formError}
        />
      )}

      {editingUser && (
        <UserFormModal
          mode="edit"
          user={editingUser}
          managers={managers}
          onSubmit={handleEdit}
          onClose={() => setEditingUser(null)}
          isPending={updateMutation.isPending}
          error={formError}
        />
      )}

      {tempPassword && (
        <TempPasswordModal
          email={tempPassword.email}
          password={tempPassword.password}
          onClose={() => setTempPassword(null)}
        />
      )}
    </div>
  );
}
