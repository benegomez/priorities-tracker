import {
  ClipboardCheck,
  CheckSquare,
  LayoutDashboard,
  FolderOpen,
  TrendingUp,
  Users,
  Building2,
  BarChart3,
  Sparkles,
  type LucideIcon,
} from "lucide-react";
import type { UserRole } from "@/store/auth-store";

export interface NavItem {
  label: string;
  href: string;
  icon: LucideIcon;
}

export interface NavGroup {
  title: string;
  items: NavItem[];
}

const employeeNav: NavGroup[] = [
  {
    title: "Mi Semana",
    items: [
      { label: "Check-In", href: "/employee/checkin", icon: ClipboardCheck },
      { label: "Check-Out", href: "/employee/checkout", icon: CheckSquare },
      { label: "Dashboard", href: "/employee/dashboard", icon: LayoutDashboard },
    ],
  },
  {
    title: "Proyectos",
    items: [
      { label: "Mis Proyectos", href: "/employee/projects", icon: FolderOpen },
    ],
  },
  {
    title: "Reportes",
    items: [
      { label: "Mi CRS", href: "/employee/crs", icon: TrendingUp },
    ],
  },
];

const managerNav: NavGroup[] = [
  {
    title: "Mi Semana",
    items: [
      { label: "Check-In", href: "/employee/checkin", icon: ClipboardCheck },
      { label: "Check-Out", href: "/employee/checkout", icon: CheckSquare },
      { label: "Mi CRS", href: "/employee/crs", icon: TrendingUp },
    ],
  },
  {
    title: "Mi Equipo",
    items: [
      { label: "Vista de Equipo", href: "/manager/team", icon: Users },
      { label: "Vista Semanal", href: "/manager/weekly", icon: LayoutDashboard },
      { label: "Resumen IA", href: "/manager/ai-summary", icon: Sparkles },
    ],
  },
  {
    title: "Proyectos",
    items: [
      { label: "Proyectos del Equipo", href: "/manager/projects", icon: FolderOpen },
    ],
  },
  {
    title: "Reportes",
    items: [
      { label: "CRS del Equipo", href: "/manager/crs", icon: TrendingUp },
      { label: "Reportes", href: "/manager/reports", icon: BarChart3 },
    ],
  },
];

const adminNav: NavGroup[] = [
  {
    title: "Organización",
    items: [
      { label: "Usuarios", href: "/admin/users", icon: Users },
      { label: "Equipos", href: "/admin/teams", icon: Building2 },
      { label: "Proyectos", href: "/admin/projects", icon: FolderOpen },
    ],
  },
  {
    title: "Reportes",
    items: [
      { label: "Reportes Generales", href: "/admin/reports", icon: BarChart3 },
    ],
  },
];

export function getNavigationForRole(role: UserRole): NavGroup[] {
  switch (role) {
    case "employee": return employeeNav;
    case "manager": return managerNav;
    case "administrator": return adminNav;
  }
}
