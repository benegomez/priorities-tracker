import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemberCRSHistory } from "@/features/teams/components/MemberCRSHistory";
import { MemberCheckInView } from "@/features/teams/components/MemberCheckInView";
import type { TeamMemberCRSHistoryItem, CheckInPriority } from "@/features/teams/services/team-service";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
  useParams: () => ({ employeeId: "emp-uuid-1" }),
}));

vi.mock("@/features/teams/hooks/useTeamMemberCRS", () => ({
  useTeamMemberCRS: vi.fn(),
}));

vi.mock("@/features/teams/hooks/useTeamMemberCheckIn", () => ({
  useTeamMemberCheckIn: vi.fn(),
}));

import { useTeamMemberCRS } from "@/features/teams/hooks/useTeamMemberCRS";
import { useTeamMemberCheckIn } from "@/features/teams/hooks/useTeamMemberCheckIn";
import TeamMemberDetailPage from "@/app/(authenticated)/manager/team/[employeeId]/page";

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

const mockHistory: TeamMemberCRSHistoryItem[] = [
  { week_start: "2025-01-06", score: 87.5, trend: "stable", risk_level: "low" },
  { week_start: "2024-12-30", score: 82.0, trend: "improving", risk_level: "low" },
];

const mockPriorities: CheckInPriority[] = [
  {
    id: "p1",
    title: "Implementar login",
    description: "OAuth2 flow",
    priority_level: "high",
    status: "in_progress",
    phase_name: "Desarrollo",
    project_name: "CRM",
    tasks: [{ id: "t1", title: "Setup OAuth", status: "completed" }],
  },
];

// ── MemberCRSHistory ──────────────────────────────────────────────────────────

describe("MemberCRSHistory", () => {
  it("renders history table rows", () => {
    render(<MemberCRSHistory history={mockHistory} />);
    expect(screen.getByText("2025-01-06")).toBeTruthy();
    expect(screen.getByText("87.5")).toBeTruthy();
    expect(screen.getByText("2024-12-30")).toBeTruthy();
    expect(screen.getByText("82.0")).toBeTruthy();
  });

  it("shows empty state when no history", () => {
    render(<MemberCRSHistory history={[]} />);
    expect(screen.getByText(/sin historial/i)).toBeTruthy();
  });
});

// ── MemberCheckInView ─────────────────────────────────────────────────────────

describe("MemberCheckInView", () => {
  it("renders priorities list", () => {
    render(<MemberCheckInView priorities={mockPriorities} weekStart="2025-01-06" status="submitted" />);
    expect(screen.getByText("Implementar login")).toBeTruthy();
    expect(screen.getByText("Setup OAuth")).toBeTruthy();
    expect(screen.getByText("CRM → Desarrollo")).toBeTruthy();
  });

  it("shows empty message when no priorities", () => {
    render(<MemberCheckInView priorities={[]} weekStart="2025-01-06" status="draft" />);
    expect(screen.getByText(/sin prioridades/i)).toBeTruthy();
  });
});

// ── TeamMemberDetailPage ──────────────────────────────────────────────────────

describe("TeamMemberDetailPage", () => {
  it("shows loading skeleton while crs is loading", () => {
    vi.mocked(useTeamMemberCRS).mockReturnValue({
      data: undefined,
      isLoading: true,
    } as unknown as ReturnType<typeof useTeamMemberCRS>);
    vi.mocked(useTeamMemberCheckIn).mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
    } as unknown as ReturnType<typeof useTeamMemberCheckIn>);
    const { container } = render(<TeamMemberDetailPage />, { wrapper });
    expect(container.querySelector(".animate-pulse")).toBeTruthy();
  });
});
