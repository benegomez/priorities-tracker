"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useUIStore } from "@/store/ui-store";
import { SidebarGroup } from "./SidebarGroup";
import { SidebarItem } from "./SidebarItem";
import { cn } from "@/lib/utils";
import type { NavGroup } from "@/config/navigation";

interface SidebarProps {
  navigation: NavGroup[];
}

export function Sidebar({ navigation }: SidebarProps) {
  const { sidebarCollapsed, toggleSidebar } = useUIStore();

  return (
    <TooltipProvider delayDuration={0}>
      <aside
        className={cn(
          "fixed left-0 top-0 z-40 hidden h-full flex-col border-r border-border bg-white transition-all duration-200 ease-in-out md:flex",
          sidebarCollapsed ? "w-[64px]" : "w-[240px]"
        )}
      >
        {/* Logo */}
        <div className="flex h-16 items-center border-b border-border px-4">
          {sidebarCollapsed ? (
            <div className="mx-auto flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-white">
              PT
            </div>
          ) : (
            <span className="text-lg font-semibold text-gray-900">Priorities Tracker</span>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-3 space-y-4">
          {navigation.map((group) => (
            <SidebarGroup key={group.title} title={group.title} collapsed={sidebarCollapsed}>
              {group.items.map((item) => (
                <SidebarItem
                  key={item.href}
                  icon={item.icon}
                  label={item.label}
                  href={item.href}
                  collapsed={sidebarCollapsed}
                />
              ))}
            </SidebarGroup>
          ))}
        </nav>

        {/* Toggle */}
        <div className="border-t border-border p-3">
          <button
            onClick={toggleSidebar}
            aria-expanded={!sidebarCollapsed}
            aria-label={sidebarCollapsed ? "Expandir sidebar" : "Colapsar sidebar"}
            className="flex w-full items-center justify-center gap-2 rounded-lg border border-border p-2 text-sm text-secondary hover:bg-primary-light hover:text-primary transition-colors"
          >
            {sidebarCollapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <>
                <ChevronLeft className="h-4 w-4" />
                <span>Colapsar</span>
              </>
            )}
          </button>
        </div>
      </aside>
    </TooltipProvider>
  );
}
