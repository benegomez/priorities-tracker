"use client";

import { cn } from "@/lib/utils";

interface SidebarGroupProps {
  title: string;
  collapsed: boolean;
  children: React.ReactNode;
}

export function SidebarGroup({ title, collapsed, children }: SidebarGroupProps) {
  return (
    <div className="space-y-1">
      {collapsed ? (
        <hr className="mx-2 border-border" />
      ) : (
        <p className={cn("px-3 py-2 text-xs font-medium uppercase tracking-wider text-secondary")}>
          {title}
        </p>
      )}
      {children}
    </div>
  );
}
