"use client";

import { useAuthStore } from "@/store/auth-store";
import { getNavigationForRole } from "@/config/navigation";
import { AppShell } from "@/components/layout/AppShell";

export default function AuthenticatedLayout({ children }: { children: React.ReactNode }) {
  const user = useAuthStore((s) => s.user);
  const role = user?.role ?? "employee";
  const navigation = getNavigationForRole(role);

  return <AppShell navigation={navigation}>{children}</AppShell>;
}
