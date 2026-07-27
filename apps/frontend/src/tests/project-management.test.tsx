import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { UserSelect } from "@/features/projects/components/UserSelect";
import type { OrgMember } from "@/features/projects/hooks/useOrgMembers";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
  useParams: () => ({ id: "project-uuid-1" }),
}));

vi.mock("@/features/projects/hooks/useProjects", () => ({
  useProjects: vi.fn(),
}));

vi.mock("@/features/projects/hooks/useProjectDetail", () => ({
  useProjectDetail: vi.fn(),
}));

vi.mock("@/features/projects/hooks/useProjectMutations", () => ({
  useCreateProject: () => ({ mutate: vi.fn(), isPending: false }),
  useUpdateProject: () => ({ mutate: vi.fn(), isPending: false }),
  useCreatePhase: () => ({ mutate: vi.fn(), isPending: false }),
  useUpdatePhase: () => ({ mutate: vi.fn(), isPending: false }),
  useAddMember: () => ({ mutate: vi.fn(), isPending: false }),
  useRemoveMember: () => ({ mutate: vi.fn(), isPending: false }),
}));

vi.mock("@/features/projects/hooks/useOrgMembers", () => ({
  useOrgMembers: () => ({ data: [] }),
}));

import { useProjects } from "@/features/projects/hooks/useProjects";
import { useProjectDetail } from "@/features/projects/hooks/useProjectDetail";
import ProjectsPage from "@/app/(authenticated)/admin/projects/page";
import ProjectDetailPage from "@/app/(authenticated)/admin/projects/[id]/page";

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

const mockMembers: OrgMember[] = [
  { id: "u1", full_name: "Ana García", role: "manager", email: "ana@test.com" },
  { id: "u2", full_name: "Juan López", role: "employee", email: "juan@test.com" },
];

// ── UserSelect ────────────────────────────────────────────────────────────────

describe("UserSelect", () => {
  it("renders placeholder when no value", () => {
    render(<UserSelect users={mockMembers} value="" onChange={vi.fn()} placeholder="Selecciona responsable..." />);
    expect(screen.getByText("Selecciona responsable...")).toBeTruthy();
  });

  it("renders user options", () => {
    render(<UserSelect users={mockMembers} value="" onChange={vi.fn()} />);
    expect(screen.getByText("Ana García (manager)")).toBeTruthy();
    expect(screen.getByText("Juan López (employee)")).toBeTruthy();
  });

  it("calls onChange when user selected", () => {
    const onChange = vi.fn();
    render(<UserSelect users={mockMembers} value="" onChange={onChange} />);
    fireEvent.change(screen.getByRole("combobox"), { target: { value: "u1" } });
    expect(onChange).toHaveBeenCalledWith("u1");
  });

  it("excludes ids from excludeIds prop", () => {
    render(<UserSelect users={mockMembers} value="" onChange={vi.fn()} excludeIds={["u1"]} />);
    expect(screen.queryByText("Ana García (manager)")).toBeNull();
    expect(screen.getByText("Juan López (employee)")).toBeTruthy();
  });
});

// ── ProjectsPage ──────────────────────────────────────────────────────────────

describe("ProjectsPage", () => {
  beforeEach(() => {
    vi.mocked(useProjects).mockReturnValue({ data: undefined, isLoading: false } as ReturnType<typeof useProjects>);
  });

  it("shows empty state when no projects", () => {
    vi.mocked(useProjects).mockReturnValue({
      data: { items: [], total: 0, page: 1, page_size: 20 },
      isLoading: false,
    } as ReturnType<typeof useProjects>);
    render(<ProjectsPage />, { wrapper });
    expect(screen.getByText(/no hay proyectos/i)).toBeTruthy();
  });

  it("renders project list with status badge", () => {
    vi.mocked(useProjects).mockReturnValue({
      data: {
        items: [
          { id: "p1", name: "Proyecto Alpha", status: "active", phases_count: 2, members_count: 3, owner: { id: "u1", full_name: "Ana García" } },
        ],
        total: 1,
        page: 1,
        page_size: 20,
      },
      isLoading: false,
    } as ReturnType<typeof useProjects>);
    render(<ProjectsPage />, { wrapper });
    expect(screen.getByText("Proyecto Alpha")).toBeTruthy();
    expect(screen.getByText("active")).toBeTruthy();
  });

  it("shows loading skeleton when loading", () => {
    vi.mocked(useProjects).mockReturnValue({ data: undefined, isLoading: true } as ReturnType<typeof useProjects>);
    const { container } = render(<ProjectsPage />, { wrapper });
    expect(container.querySelector(".animate-pulse")).toBeTruthy();
  });
});

// ── ProjectDetailPage ─────────────────────────────────────────────────────────

describe("ProjectDetailPage", () => {
  const mockProject = {
    id: "project-uuid-1",
    name: "Proyecto Beta",
    description: "Descripción del proyecto",
    status: "active",
    owner: { id: "u1", full_name: "Ana García" },
    phases: [
      { id: "ph1", name: "Fase Diseño", status: "planned" },
      { id: "ph2", name: "Fase Desarrollo", status: "active" },
    ],
    members: [
      { user_id: "u2", full_name: "Juan López", role: "employee" },
    ],
    created_at: "2025-01-01T00:00:00Z",
    updated_at: "2025-01-01T00:00:00Z",
  };

  beforeEach(() => {
    vi.mocked(useProjectDetail).mockReturnValue({ data: mockProject, isLoading: false } as ReturnType<typeof useProjectDetail>);
  });

  it("renders project name and status", () => {
    render(<ProjectDetailPage />, { wrapper });
    expect(screen.getByText("Proyecto Beta")).toBeTruthy();
    expect(screen.getAllByText("active").length).toBeGreaterThan(0);
  });

  it("renders phases list", () => {
    render(<ProjectDetailPage />, { wrapper });
    expect(screen.getByText("Fase Diseño")).toBeTruthy();
    expect(screen.getByText("Fase Desarrollo")).toBeTruthy();
  });

  it("renders members list", () => {
    render(<ProjectDetailPage />, { wrapper });
    expect(screen.getByText("Juan López")).toBeTruthy();
  });

  it("shows loading skeleton when loading", () => {
    vi.mocked(useProjectDetail).mockReturnValue({ data: undefined, isLoading: true } as ReturnType<typeof useProjectDetail>);
    const { container } = render(<ProjectDetailPage />, { wrapper });
    expect(container.querySelector(".animate-pulse")).toBeTruthy();
  });
});
