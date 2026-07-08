import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { DashboardWeekCard } from "@/features/dashboard/components/DashboardWeekCard";
import { DashboardPrioritiesList } from "@/features/dashboard/components/DashboardPrioritiesList";
import type { CheckInResponse } from "@/features/checkins/services/checkin-service";
import type { CRSCurrentResponse } from "@/features/crs/services/crs-service";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

const mockCheckIn: CheckInResponse = {
  id: "ci1",
  employee_id: "u1",
  organization_id: "o1",
  week_start: "2026-07-07",
  status: "submitted",
  submitted_at: "2026-07-07T10:00:00Z",
  priorities_count: 3,
  priorities: [
    { id: "p1", title: "Priority A", description: null, priority_level: "high", status: "completed", phase_name: null, project_name: null, tasks: [] },
    { id: "p2", title: "Priority B", description: null, priority_level: "medium", status: "in_progress", phase_name: null, project_name: null, tasks: [] },
    { id: "p3", title: "Priority C", description: null, priority_level: "low", status: "planned", phase_name: null, project_name: null, tasks: [] },
  ],
  created_at: "2026-07-07T09:00:00Z",
  updated_at: "2026-07-07T10:00:00Z",
};

const mockCRS: CRSCurrentResponse = {
  score: 85.0,
  trend: "improving",
  risk_level: "low",
  week_start: "2026-07-07",
  formula_version: "v1.0",
  priorities_total: 3,
  priorities_completed: 2,
  tasks_total: 5,
  tasks_completed: 4,
};

// ── DashboardWeekCard ──────────────────────────────────────────────────────────

describe("DashboardWeekCard", () => {
  it("shows create checkin CTA when no checkin (404)", () => {
    const error404 = { status: 404, error_code: "NOT_FOUND", message: "Not found" };
    render(
      <DashboardWeekCard
        checkInData={undefined}
        checkInLoading={false}
        checkInError={error404}
        crsData={undefined}
      />,
      { wrapper },
    );
    expect(screen.getByText(/no has creado tu check-in/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /crear check-in/i })).toBeInTheDocument();
  });

  it("shows submit CTA when checkin is draft", () => {
    const draftCheckIn = { ...mockCheckIn, status: "draft" as const };
    render(
      <DashboardWeekCard
        checkInData={draftCheckIn}
        checkInLoading={false}
        checkInError={null}
        crsData={undefined}
      />,
      { wrapper },
    );
    expect(screen.getByRole("link", { name: /enviar check-in/i })).toBeInTheDocument();
  });

  it("shows checkout CTA when checkin submitted but no CRS for this week", () => {
    render(
      <DashboardWeekCard
        checkInData={mockCheckIn}
        checkInLoading={false}
        checkInError={null}
        crsData={undefined}
      />,
      { wrapper },
    );
    expect(screen.getByRole("link", { name: /completar check-out/i })).toBeInTheDocument();
  });

  it("shows completed badge when checkin submitted and CRS week matches", () => {
    render(
      <DashboardWeekCard
        checkInData={mockCheckIn}
        checkInLoading={false}
        checkInError={null}
        crsData={mockCRS}
      />,
      { wrapper },
    );
    expect(screen.getByText(/semana completada/i)).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: /check-out/i })).not.toBeInTheDocument();
  });

  it("shows skeleton when loading", () => {
    const { container } = render(
      <DashboardWeekCard
        checkInData={undefined}
        checkInLoading={true}
        checkInError={null}
        crsData={undefined}
      />,
      { wrapper },
    );
    expect(container.querySelector(".animate-pulse")).toBeInTheDocument();
  });
});

// ── DashboardPrioritiesList ────────────────────────────────────────────────────

describe("DashboardPrioritiesList", () => {
  it("shows correct counters", () => {
    render(
      <DashboardPrioritiesList priorities={mockCheckIn.priorities} checkinId="ci1" />,
      { wrapper },
    );
    // 1 completed, 1 in_progress out of 3
    expect(screen.getByText(/1\/3 completadas/i)).toBeInTheDocument();
    expect(screen.getByText(/1 en progreso/i)).toBeInTheDocument();
  });

  it("shows empty state when no priorities", () => {
    render(
      <DashboardPrioritiesList priorities={[]} checkinId="ci1" />,
      { wrapper },
    );
    expect(screen.getByText(/no hay prioridades/i)).toBeInTheDocument();
  });

  it("renders priority titles", () => {
    render(
      <DashboardPrioritiesList priorities={mockCheckIn.priorities} checkinId="ci1" />,
      { wrapper },
    );
    expect(screen.getByText("Priority A")).toBeInTheDocument();
    expect(screen.getByText("Priority B")).toBeInTheDocument();
  });
});
