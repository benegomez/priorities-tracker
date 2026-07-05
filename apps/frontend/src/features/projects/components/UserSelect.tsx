"use client";

import type { OrgMember } from "../hooks/useOrgMembers";

interface UserSelectProps {
  users: OrgMember[];
  value: string;
  onChange: (userId: string) => void;
  placeholder?: string;
  excludeIds?: string[];
  disabled?: boolean;
}

export function UserSelect({ users, value, onChange, placeholder = "Selecciona un usuario...", excludeIds = [], disabled = false }: UserSelectProps) {
  const filtered = users.filter((u) => !excludeIds.includes(u.id));

  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full rounded-lg border border-border px-3 py-2 text-sm disabled:opacity-50"
      disabled={disabled || filtered.length === 0}
    >
      <option value="">{filtered.length === 0 ? "No hay usuarios disponibles" : placeholder}</option>
      {filtered.map((user) => (
        <option key={user.id} value={user.id}>
          {user.full_name} ({user.role})
        </option>
      ))}
    </select>
  );
}
