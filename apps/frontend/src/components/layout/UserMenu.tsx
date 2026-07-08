"use client";

import { useEffect, useRef, useState } from "react";
import { LogOut } from "lucide-react";
import { useAuthStore } from "@/store/auth-store";
import { useLogout } from "@/features/auth/hooks/useLogout";
import { Badge } from "@/components/ui/badge";

export function UserMenu() {
  const user = useAuthStore((s) => s.user);
  const { mutate, isPending } = useLogout();
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const initials = user
    ? user.full_name.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase()
    : "??";

  useEffect(() => {
    if (!open) return;
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEscape);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);
    };
  }, [open]);

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-haspopup="menu"
        aria-label="Menú de usuario"
        className="flex items-center gap-3 rounded-lg p-1 hover:bg-gray-50 transition-colors"
      >
        <div className="hidden sm:block text-right">
          <p className="text-sm font-medium text-gray-900">{user?.full_name}</p>
          <Badge variant="outline" className="text-xs">{user?.role}</Badge>
        </div>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-xs font-medium text-white">
          {initials}
        </div>
      </button>

      {open && (
        <div
          role="menu"
          className="absolute right-0 top-full mt-2 w-48 rounded-lg border border-border bg-white py-1 shadow-lg z-50"
        >
          <button
            role="menuitem"
            onClick={() => mutate()}
            disabled={isPending}
            className="flex w-full items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LogOut className="h-4 w-4" />
            {isPending ? "Cerrando..." : "Cerrar sesión"}
          </button>
        </div>
      )}
    </div>
  );
}
