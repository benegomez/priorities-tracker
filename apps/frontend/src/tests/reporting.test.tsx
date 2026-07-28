import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReportStatCard } from "@/features/reports/components/ReportStatCard";
import { ReportWeeklyBreakdown } from "@/features/reports/components/ReportWeeklyBreakdown";
import type { WeeklyBreakdownItem } from "@/features/reports/services/report-service";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

vi.mock("@/features/reports/hooks/useIndividualReport", () => ({
  useIndividualReport: vi.fn(),
}));

vi.mock("@/features/reports/hooks/useTeamReport", () => ({
  useTeamReport: vi.fn(),
}));

import { useIndividualReport } from "@/features/reports/hooks/useIndividualReport";
import { useTeamReport } from "@/features/reports/hooks/useTeamReport";
import EmployeeReportsPage from "@/app/(authenticated)/employee/reports/page";
import ManagerReportsPage from "@/app/(authenticated)/manager/reports/page";

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

const sampleRows: WeeklyBreakdownItem[] = [
  { week_start: "2025-01-06", committed: 4, completed: 3, carried_over: 1, crs: 82.5 },
  { week_start: "2025-01-13", committed: 3, completed: 3, carried_over: 0, crs: 90.0 },
];

// ── ReportStatCard ────────────────────────────────────────────────────────────

describe("ReportStatCard", () => {
  it("renders label and value", () => {
    render(<ReportStatCard label="Tasa de cumplimiento" value="83%" />);
    expect(screen.getByText("Tasa de cumplimiento")).toBeTruthy();
    expect(screen.getByText("83%")).toBeTruthy();
  });

  it("renders sublabel when provided", () => {
    render(<ReportStatCard label="CRS" value={88} sublabel="improving" />);
    expect(screen.getByText("improving")).toBeTruthy();
  });
});

// ── ReportWeeklyBreakdown ─────────────────────────────────────────────────────

describe("ReportWeeklyBreakdown", () => {
  it("renders table rows", () => {
    render(<ReportWeeklyBreakdown rows={sampleRows} />);
    expect(screen.getByText("2025-01-06")).toBeTruthy();
    expect(screen.getByText("2025-01-13")).toBeTruthy();
    expect(screen.getByText("82.5")).toBeTruthy();
  });

  it("shows empty state when no rows", () => {
    render(<ReportWeeklyBreakdown rows={[]} />);
    expect(screen.getByText(/sin datos/i)).toBeTruthy();
  });
});

// ── EmployeeReportsPage ───────────────────────────────────────────────────────

describe("EmployeeReportsPage", () => {
  it("shows loading skeleton", () => {
    vi.mocked(useIndividualReport).mockReturnValue({
      data: undefined,
      isLoading: true,
    } as unknown as ReturnType<typeof useIndividualReport>);
    render(<EmployeeReportsPage />, { wrapper });
    expect(screen.getByLabelText("Cargando reporte")).toBeTruthy();
  });

  it("renders stats when data loaded", () => {
    vi.mocked(useIndividualReport).mockReturnValue({
      data: {
        employee: { id: "u1", first_name: "Ana", last_name: "García" },
        period_weeks: 8,
        total_priorities: 20,
        completed_priorities: 17,
        completion_rate: 85.0,
        carried_over_count: 3,
        crs_current: 88.5,
        crs_trend: "improving",
        weekly_breakdown: sampleRows,
      },
      isLoading: false,
    } as unknown as ReturnType<typeof useIndividualReport>);
    render(<EmployeeReportsPage />, { wrapper });
    expect(screen.getByText("20")).toBeTruthy();
    expect(screen.getByText("85.0%")).toBeTruthy();
  });
});

// ── ManagerReportsPage ────────────────────────────────────────────────────────

describe("ManagerReportsPage", () => {
  it("shows empty state when no team members", () => {
    vi.mocked(useTeamReport).mockReturnValue({
      data: {
        team_size: 0,
        period_weeks: 8,
        avg_completion_rate: 0,
        avg_crs: null,
        members: [],
        weekly_breakdown: [],
      },
      isLoading: false,
    } as unknown as ReturnType<typeof useTeamReport>);
    render(<ManagerReportsPage />, { wrapper });
    expect(screen.getByText(/sin miembros/i)).toBeTruthy();
  });
});
