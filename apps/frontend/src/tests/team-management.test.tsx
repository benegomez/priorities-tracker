import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { AdminTeamTable } from "@/features/teams/components/AdminTeamTable";
import { TeamFormModal } from "@/features/teams/components/TeamFormModal";
import { TeamMembersModal } from "@/features/teams/components/TeamMembersModal";
import type { AdminTeamResponse, AdminTeamDetailResponse } from "@/features/teams/services/team-service";
import type { UserResponse } from "@/features/users/services/user-service";

const mockTeam: AdminTeamResponse = {
  id: "team-1",
  name: "Equipo Alpha",
  manager_id: "mgr-1",
  manager_name: "Ana García",
  member_count: 3,
  created_at: "2025-01-01T00:00:00Z",
  updated_at: "2025-01-01T00:00:00Z",
};

const mockTeamDetail: AdminTeamDetailResponse = {
  ...mockTeam,
  members: [
    { id: "usr-1", first_name: "Juan", last_name: "Lopez", role: "employee", status: "active" },
    { id: "usr-2", first_name: "Maria", last_name: "Gomez", role: "employee", status: "active" },
  ],
};

const mockManager: UserResponse = {
  id: "mgr-1",
  email: "ana@test.com",
  first_name: "Ana",
  last_name: "García",
  role: "manager",
  status: "active",
  manager_id: null,
  manager_name: null,
  created_at: null,
  updated_at: null,
};

const tableDefaults = {
  teams: [mockTeam],
  total: 1,
  page: 1,
  pages: 1,
  onPageChange: vi.fn(),
  onEdit: vi.fn(),
  onViewMembers: vi.fn(),
};

// ── AdminTeamTable ────────────────────────────────────────────────────────────

describe("AdminTeamTable", () => {
  it("renders team list", () => {
    render(<AdminTeamTable {...tableDefaults} />);
    expect(screen.getByText("Equipo Alpha")).toBeTruthy();
    expect(screen.getByText("Ana García")).toBeTruthy();
  });

  it("shows member count", () => {
    render(<AdminTeamTable {...tableDefaults} />);
    expect(screen.getByText("3")).toBeTruthy();
  });

  it("shows empty state when no teams", () => {
    render(<AdminTeamTable {...tableDefaults} teams={[]} total={0} />);
    expect(screen.getByText(/no hay equipos/i)).toBeTruthy();
  });
});

// ── TeamFormModal ─────────────────────────────────────────────────────────────

describe("TeamFormModal", () => {
  it("renders create mode", () => {
    render(
      <TeamFormModal
        mode="create"
        managers={[]}
        onSubmit={vi.fn()}
        onClose={vi.fn()}
        isPending={false}
      />
    );
    expect(screen.getByLabelText(/crear equipo/i)).toBeTruthy();
    expect(screen.getByText("Crear Equipo")).toBeTruthy();
  });

  it("renders edit mode with existing data", () => {
    render(
      <TeamFormModal
        mode="edit"
        team={mockTeam}
        managers={[mockManager]}
        onSubmit={vi.fn()}
        onClose={vi.fn()}
        isPending={false}
      />
    );
    expect(screen.getByDisplayValue("Equipo Alpha")).toBeTruthy();
    expect(screen.getByText("Guardar Cambios")).toBeTruthy();
  });

  it("calls onSubmit with correct data on create", () => {
    const onSubmit = vi.fn();
    render(
      <TeamFormModal
        mode="create"
        managers={[]}
        onSubmit={onSubmit}
        onClose={vi.fn()}
        isPending={false}
      />
    );
    fireEvent.change(screen.getByPlaceholderText("Nombre del equipo"), {
      target: { value: "Nuevo Equipo" },
    });
    fireEvent.click(screen.getByText("Crear Equipo"));
    expect(onSubmit).toHaveBeenCalledWith({ name: "Nuevo Equipo" });
  });
});

// ── TeamMembersModal ──────────────────────────────────────────────────────────

describe("TeamMembersModal", () => {
  const membersDefaults = {
    team: mockTeamDetail,
    allUsers: [mockManager],
    onAddMember: vi.fn(),
    onRemoveMember: vi.fn(),
    onClose: vi.fn(),
    isAddPending: false,
    isRemovingId: null,
  };

  it("renders member list", () => {
    render(<TeamMembersModal {...membersDefaults} />);
    expect(screen.getByText(/Juan Lopez/)).toBeTruthy();
    expect(screen.getByText(/Maria Gomez/)).toBeTruthy();
  });

  it("calls onRemoveMember when remove clicked", () => {
    const onRemoveMember = vi.fn();
    render(<TeamMembersModal {...membersDefaults} onRemoveMember={onRemoveMember} />);
    fireEvent.click(screen.getAllByText("Remover")[0]);
    expect(onRemoveMember).toHaveBeenCalledWith("usr-1");
  });
});
