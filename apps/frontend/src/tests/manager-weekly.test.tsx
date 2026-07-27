import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { WeeklySummaryBar } from "@/features/teams/components/WeeklySummaryBar";
import { WeeklyMemberRow } from "@/features/teams/components/WeeklyMemberRow";
import type { TeamMember } from "@/features/teams/services/team-service";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

vi.mock("@/features/teams/hooks/useMyTeam", () => ({
  useMyTeam: vi.fn(),
}));

vi.mock("@/features/teams/hooks/useTeamMemberCheckIn", () => ({
  useTeamMemberCheckIn: vi.fn(),
}));

import { useMyTeam } from "@/features/teams/hooks/useMyTeam";
import { useTeamMemberCheckIn } from "@/features/teams/hooks/useTeamMemberCheckIn";
import ManagerWeeklyPage from "@/app/(authenticated)/manager/weekly/page";

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

const memberWithCheckIn: TeamMember = {
  id: "m1",
  first_name: "Ana",
  last_name: "García",
  email: "ana@test.com",
  crs: { score: 85, trend: "stable", risk_level: "low" },
  week_status: { week_start: "2025-01-06", checkin_status: "submitted", checkout_status: null },
};

const memberWithoutCheckIn: TeamMember = {
  id: "m2",
  first_name: "Juan",
  last_name: "López",
  email: "juan@test.com",
  crs: null,
  week_status: { week_start: "2025-01-06", checkin_status: null, checkout_status: null },
};

// ── WeeklySummaryBar ──────────────────────────────────────────────────────────

describe("WeeklySummaryBar", () => {
  it("renders correct counts", () => {
    render(<WeeklySummaryBar total={5} checkins={3} checkouts={2} />);
    expect(screen.getByText("3/5")).toBeTruthy();
    expect(screen.getByText("2/5")).toBeTruthy();
  });

  it("shows all members checked in", () => {
    render(<WeeklySummaryBar total={4} checkins={4} checkouts={4} />);
    const counts = screen.getAllByText("4/4");
    expect(counts.length).toBe(2);
  });
});

// ── WeeklyMemberRow ───────────────────────────────────────────────────────────

describe("WeeklyMemberRow", () => {
  beforeEach(() => {
    vi.mocked(useTeamMemberCheckIn).mockReturnValue({
      data: undefined,
      isLoading: false,
    } as ReturnType<typeof useTeamMemberCheckIn>);
  });

  it("renders member name and checkin badge", () => {
    render(
      <table><tbody>
        <WeeklyMemberRow member={memberWithCheckIn} isExpanded={false} onToggle={vi.fn()} />
      </tbody></table>,
      { wrapper }
    );
    expect(screen.getByText("Ana García")).toBeTruthy();
    expect(screen.getByLabelText("Check-In: Enviado")).toBeTruthy();
  });

  it("shows alert when no checkin", () => {
    render(
      <table><tbody>
        <WeeklyMemberRow member={memberWithoutCheckIn} isExpanded={false} onToggle={vi.fn()} />
      </tbody></table>,
      { wrapper }
    );
    expect(screen.getByRole("alert")).toBeTruthy();
    expect(screen.getByText(/sin check-in/i)).toBeTruthy();
  });

  it("is not expandable without checkin", () => {
    const onToggle = vi.fn();
    render(
      <table><tbody>
        <WeeklyMemberRow member={memberWithoutCheckIn} isExpanded={false} onToggle={onToggle} />
      </tbody></table>,
      { wrapper }
    );
    fireEvent.click(screen.getByText("Juan López"));
    expect(onToggle).not.toHaveBeenCalled();
  });

  it("calls onToggle when clicked with checkin", () => {
    const onToggle = vi.fn();
    render(
      <table><tbody>
        <WeeklyMemberRow member={memberWithCheckIn} isExpanded={false} onToggle={onToggle} />
      </tbody></table>,
      { wrapper }
    );
    fireEvent.click(screen.getByText("Ana García"));
    expect(onToggle).toHaveBeenCalledOnce();
  });
});

// ── ManagerWeeklyPage ─────────────────────────────────────────────────────────

describe("ManagerWeeklyPage", () => {
  it("shows empty state when no members", () => {
    vi.mocked(useMyTeam).mockReturnValue({
      data: { members: [] },
      isLoading: false,
      error: null,
    } as unknown as ReturnType<typeof useMyTeam>);
    render(<ManagerWeeklyPage />, { wrapper });
    // TeamEmptyState renders when members is empty
    expect(screen.getByText(/vista semanal/i)).toBeTruthy();
    expect(screen.queryByText(/resumen semanal/i)).toBeNull();
  });
});
