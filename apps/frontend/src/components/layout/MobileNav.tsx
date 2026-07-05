"use client";

import { useEffect } from "react";
import { X } from "lucide-react";
import { useUIStore } from "@/store/ui-store";
import { SidebarGroup } from "./SidebarGroup";
import { SidebarItem } from "./SidebarItem";
import { cn } from "@/lib/utils";
import type { NavGroup } from "@/config/navigation";

interface MobileNavProps {
  navigation: NavGroup[];
}

export function MobileNav({ navigation }: MobileNavProps) {
  const { mobileNavOpen, setMobileNavOpen } = useUIStore();

  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") setMobileNavOpen(false);
    }
    if (mobileNavOpen) {
      document.addEventListener("keydown", handleEscape);
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "";
    };
  }, [mobileNavOpen, setMobileNavOpen]);

  if (!mobileNavOpen) return null;

  return (
    <div className="fixed inset-0 z-50 md:hidden" role="dialog" aria-modal="true">
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/50 transition-opacity"
        onClick={() => setMobileNavOpen(false)}
        aria-hidden="true"
      />

      {/* Panel */}
      <nav
        className={cn(
          "fixed left-0 top-0 h-full w-72 bg-white shadow-xl transition-transform duration-200 ease-in-out",
          mobileNavOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Header */}
        <div className="flex h-16 items-center justify-between border-b border-border px-4">
          <span className="text-lg font-semibold text-gray-900">Priorities Tracker</span>
          <button
            onClick={() => setMobileNavOpen(false)}
            className="rounded-lg p-2 text-secondary hover:bg-gray-100"
            aria-label="Cerrar menú"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation */}
        <div className="overflow-y-auto p-3 space-y-4">
          {navigation.map((group) => (
            <SidebarGroup key={group.title} title={group.title} collapsed={false}>
              {group.items.map((item) => (
                <div key={item.href} onClick={() => setMobileNavOpen(false)}>
                  <SidebarItem
                    icon={item.icon}
                    label={item.label}
                    href={item.href}
                    collapsed={false}
                  />
                </div>
              ))}
            </SidebarGroup>
          ))}
        </div>
      </nav>
    </div>
  );
}
