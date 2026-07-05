import { describe, it, expect, vi, beforeEach, beforeAll } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { getNavigationForRole } from "@/config/navigation";

// Mock next/navigation
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
  usePathname: () => "/employee/checkin",
}));

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

describe("navigation config", () => {
  it("returns correct items for employee", () => {
    const nav = getNavigationForRole("employee");
    expect(nav).toHaveLength(3);
    expect(nav[0].title).toBe("Mi Semana");
    expect(nav[0].items).toHaveLength(3);
    expect(nav[0].items[0].label).toBe("Check-In");
    expect(nav[0].items[0].href).toBe("/employee/checkin");
    expect(nav[0].items[1].label).toBe("Check-Out");
  });

  it("returns correct items for manager", () => {
    const nav = getNavigationForRole("manager");
    expect(nav).toHaveLength(3);
    expect(nav[0].title).toBe("Mi Equipo");
    expect(nav[0].items[0].label).toBe("Vista de Equipo");
  });

  it("returns correct items for administrator", () => {
    const nav = getNavigationForRole("administrator");
    expect(nav).toHaveLength(2);
    expect(nav[0].title).toBe("Organización");
    expect(nav[0].items).toHaveLength(3);
  });
});

describe("ui-store", () => {
  it("toggles sidebar state", async () => {
    const { useUIStore } = await import("@/store/ui-store");
    useUIStore.getState().setSidebarCollapsed(false);
    useUIStore.getState().toggleSidebar();
    expect(useUIStore.getState().sidebarCollapsed).toBe(true);
    useUIStore.getState().toggleSidebar();
    expect(useUIStore.getState().sidebarCollapsed).toBe(false);
  });

  it("sets mobile nav open", async () => {
    const { useUIStore } = await import("@/store/ui-store");
    useUIStore.getState().setMobileNavOpen(true);
    expect(useUIStore.getState().mobileNavOpen).toBe(true);
    useUIStore.getState().setMobileNavOpen(false);
    expect(useUIStore.getState().mobileNavOpen).toBe(false);
  });

  it("sets sidebar collapsed directly", async () => {
    const { useUIStore } = await import("@/store/ui-store");
    useUIStore.getState().setSidebarCollapsed(true);
    expect(useUIStore.getState().sidebarCollapsed).toBe(true);
  });
});

describe("SidebarGroup", () => {
  it("renders group title when expanded", async () => {
    const { SidebarGroup } = await import("@/components/layout/SidebarGroup");
    render(<SidebarGroup title="Mi Semana" collapsed={false}><div>item</div></SidebarGroup>);
    expect(screen.getByText("Mi Semana")).toBeInTheDocument();
  });

  it("renders separator when collapsed", async () => {
    const { SidebarGroup } = await import("@/components/layout/SidebarGroup");
    const { container } = render(<SidebarGroup title="Mi Semana" collapsed={true}><div>item</div></SidebarGroup>);
    expect(container.querySelector("hr")).toBeInTheDocument();
    expect(screen.queryByText("Mi Semana")).not.toBeInTheDocument();
  });
});

describe("Header", () => {
  beforeEach(async () => {
    const { useAuthStore } = await import("@/store/auth-store");
    useAuthStore.setState({
      user: { id: "1", email: "test@test.com", role: "employee", organization_id: "org1", full_name: "Juan Pérez" },
    });
  });

  it("renders user name and initials", async () => {
    const { Header } = await import("@/components/layout/Header");
    render(<Header />, { wrapper });
    expect(screen.getByText("Juan Pérez")).toBeInTheDocument();
    expect(screen.getByText("JP")).toBeInTheDocument();
  });

  it("renders hamburger button for mobile", async () => {
    const { Header } = await import("@/components/layout/Header");
    render(<Header />, { wrapper });
    expect(screen.getByLabelText("Abrir menú de navegación")).toBeInTheDocument();
  });
});
