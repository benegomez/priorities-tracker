"use client";

import { Menu } from "lucide-react";
import { useUIStore } from "@/store/ui-store";
import { UserMenu } from "./UserMenu";

export function Header() {
  const setMobileNavOpen = useUIStore((s) => s.setMobileNavOpen);

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

      {/* User menu with logout */}
      <UserMenu />
    </header>
  );
}
