"use client";

import { useEffect } from "react";
import { useUIStore } from "@/store/ui-store";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { MobileNav } from "./MobileNav";
import { cn } from "@/lib/utils";
import type { NavGroup } from "@/config/navigation";

interface AppShellProps {
  navigation: NavGroup[];
  children: React.ReactNode;
}

export function AppShell({ navigation, children }: AppShellProps) {
  const { sidebarCollapsed, setSidebarCollapsed } = useUIStore();

  // Detect initial breakpoint
  useEffect(() => {
    const xl = window.matchMedia("(min-width: 1280px)");
    const md = window.matchMedia("(min-width: 768px)");

    function handleResize() {
      if (xl.matches) {
        setSidebarCollapsed(false);
      } else if (md.matches) {
        setSidebarCollapsed(true);
      }
    }

    // Only set default on first load if no persisted preference
    const stored = localStorage.getItem("pt-ui-store");
    if (!stored) handleResize();

    xl.addEventListener("change", handleResize);
    return () => xl.removeEventListener("change", handleResize);
  }, [setSidebarCollapsed]);

  return (
    <div className="min-h-screen bg-surface">
      <Sidebar navigation={navigation} />
      <MobileNav navigation={navigation} />

      <div
        className={cn(
          "flex flex-col transition-all duration-200 ease-in-out",
          "md:ml-[64px]",
          !sidebarCollapsed && "md:ml-[240px]"
        )}
      >
        <Header />
        <main className="flex-1 p-4 md:p-6">
          <div className="mx-auto max-w-4xl">{children}</div>
        </main>
      </div>
    </div>
  );
}
