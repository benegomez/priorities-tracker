import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

vi.mock("@/features/reports/hooks/useTeamReport", () => ({
  useTeamReport: vi.fn(),
}));

import { useTeamReport } from "@/features/reports/hooks/useTeamReport";
import ManagerTeamCRSPage from "@/app/(authenticated)/manager/crs/page";

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

const mockData = {
  team_size: 3,
  period_weeks: 8,
  avg_completion_rate: 78.0,
  avg_crs: 74.5,
  weekly_breakdown: [],
  members: [
    { id: "m1", first_name: "Ana", last_name: "García", completion_rate: 90.0, crs: 88.0, trend: "improving" },
    { id: "m2", first_name: "Juan", last_name: "López", completion_rate: 62.0, crs: 54.0, trend: "declining" },
    { id: "m3", first_name: "Luis", last_name: "Pérez", completion_rate: 70.0, crs: null, trend: null },
  ],
};

// ── ManagerTeamCRSPage ────────────────────────────────────────────────────────

describe("ManagerTeamCRSPage", () => {
  it("shows loading skeleton", () => {
    vi.mocked(useTeamReport).mockReturnValue({
      data: undefined,
      isLoading: true,
    } as unknown as ReturnType<typeof useTeamReport>);
    render(<ManagerTeamCRSPage />, { wrapper });
    expect(screen.getByLabelText("Cargando CRS del equipo")).toBeTruthy();
  });

  it("renders avg CRS stat card", () => {
    vi.mocked(useTeamReport).mockReturnValue({
      data: mockData,
      isLoading: false,
    } as unknown as ReturnType<typeof useTeamReport>);
    render(<ManagerTeamCRSPage />, { wrapper });
    expect(screen.getByText("CRS Promedio")).toBeTruthy();
    expect(screen.getByText("74.5")).toBeTruthy();
  });

  it("renders member rows sorted by CRS ascending (nulls first)", () => {
    vi.mocked(useTeamReport).mockReturnValue({
      data: mockData,
      isLoading: false,
    } as unknown as ReturnType<typeof useTeamReport>);
    render(<ManagerTeamCRSPage />, { wrapper });
    const rows = screen.getAllByRole("row").slice(1); // skip header
    // null CRS first, then 54.0, then 88.0
    expect(rows[0].textContent).toContain("Luis Pérez");
    expect(rows[1].textContent).toContain("Juan López");
    expect(rows[2].textContent).toContain("Ana García");
  });

  it("shows empty state when no members", () => {
    vi.mocked(useTeamReport).mockReturnValue({
      data: { ...mockData, team_size: 0, members: [] },
      isLoading: false,
    } as unknown as ReturnType<typeof useTeamReport>);
    render(<ManagerTeamCRSPage />, { wrapper });
    expect(screen.getByText(/no tienes miembros/i)).toBeTruthy();
  });
});
