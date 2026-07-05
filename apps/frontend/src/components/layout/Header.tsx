"use client";

import { Menu } from "lucide-react";
import { useAuthStore } from "@/store/auth-store";
import { useUIStore } from "@/store/ui-store";
import { Badge } from "@/components/ui/badge";

export function Header() {
  const user = useAuthStore((s) => s.user);
  const setMobileNavOpen = useUIStore((s) => s.setMobileNavOpen);

  const initials = user
    ? `${user.full_name.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase()}`
    : "??";

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-white px-4 md:px-6">
      {/* Mobile hamburger */}
      <button
        onClick={() => setMobileNavOpen(true)}
        className="rounded-lg p-2 text-secondary hover:bg-gray-100 md:hidden"
        aria-label="Abrir menú de navegación"
      >
        <Menu className="h-5 w-5" />
      </button>

      {/* Spacer for desktop */}
      <div className="hidden md:block" />

      {/* User info */}
      <div className="flex items-center gap-3">
        <div className="hidden sm:block text-right">
          <p className="text-sm font-medium text-gray-900">{user?.full_name}</p>
          <Badge variant="outline" className="text-xs">{user?.role}</Badge>
        </div>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-xs font-medium text-white">
          {initials}
        </div>
      </div>
    </header>
  );
}
