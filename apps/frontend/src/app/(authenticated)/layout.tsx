"use client";

import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/auth-store";
import { getNavigationForRole } from "@/config/navigation";
import { AppShell } from "@/components/layout/AppShell";
import type { UserRole } from "@/store/auth-store";

export default function AuthenticatedLayout({ children }: { children: React.ReactNode }) {
  const user = useAuthStore((s) => s.user);
  const [cookieRole, setCookieRole] = useState<UserRole>("employee");

  useEffect(() => {
    const match = document.cookie.match(/user_role=([^;]+)/);
    if (match) setCookieRole(match[1] as UserRole);
  }, []);

  const role = user?.role ?? cookieRole;
  const navigation = getNavigationForRole(role);

  return <AppShell navigation={navigation}>{children}</AppShell>;
}
