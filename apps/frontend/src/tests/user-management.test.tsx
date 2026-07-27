import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { UserStatusBadge } from "@/features/users/components/UserStatusBadge";
import { UserFormModal } from "@/features/users/components/UserFormModal";
import { TempPasswordModal } from "@/features/users/components/TempPasswordModal";
import { UserTable } from "@/features/users/components/UserTable";
import type { UserResponse } from "@/features/users/services/user-service";

const mockUser: UserResponse = {
  id: "uuid-1",
  email: "juan@test.com",
  first_name: "Juan",
  last_name: "Lopez",
  role: "employee",
  status: "active",
  manager_id: null,
  manager_name: null,
  created_at: null,
  updated_at: null,
};

const mockInactiveUser: UserResponse = { ...mockUser, id: "uuid-2", first_name: "Maria", last_name: "Gomez", email: "maria@test.com", status: "inactive" };

// ── UserStatusBadge ───────────────────────────────────────────────────────────

describe("UserStatusBadge", () => {
  it("renders active badge", () => {
    render(<UserStatusBadge status="active" />);
    expect(screen.getByText("Activo")).toBeTruthy();
  });

  it("renders inactive badge", () => {
    render(<UserStatusBadge status="inactive" />);
    expect(screen.getByText("Inactivo")).toBeTruthy();
  });
});

// ── UserFormModal ─────────────────────────────────────────────────────────────

describe("UserFormModal", () => {
  it("renders create form with required fields", () => {
    render(
      <UserFormModal
        mode="create"
        managers={[]}
        onSubmit={vi.fn()}
        onClose={vi.fn()}
        isPending={false}
      />
    );
    expect(screen.getByLabelText(/crear usuario/i)).toBeTruthy();
    expect(screen.getByPlaceholderText(/usuario@empresa.com/i)).toBeTruthy();
    expect(screen.getByText("Crear Usuario")).toBeTruthy();
  });

  it("renders edit form with user data", () => {
    render(
      <UserFormModal
        mode="edit"
        user={mockUser}
        managers={[]}
        onSubmit={vi.fn()}
        onClose={vi.fn()}
        isPending={false}
      />
    );
    expect(screen.getByDisplayValue("Juan")).toBeTruthy();
    expect(screen.getByDisplayValue("Lopez")).toBeTruthy();
    expect(screen.getByText("Guardar Cambios")).toBeTruthy();
  });

  it("shows error message when provided", () => {
    render(
      <UserFormModal
        mode="create"
        managers={[]}
        onSubmit={vi.fn()}
        onClose={vi.fn()}
        isPending={false}
        error="Email ya existe en la organización"
      />
    );
    expect(screen.getByText("Email ya existe en la organización")).toBeTruthy();
  });

  it("calls onClose when cancel is clicked", () => {
    const onClose = vi.fn();
    render(
      <UserFormModal
        mode="create"
        managers={[]}
        onSubmit={vi.fn()}
        onClose={onClose}
        isPending={false}
      />
    );
    fireEvent.click(screen.getByText("Cancelar"));
    expect(onClose).toHaveBeenCalledOnce();
  });
});

// ── TempPasswordModal ─────────────────────────────────────────────────────────

describe("TempPasswordModal", () => {
  it("shows email and temporary password", () => {
    render(
      <TempPasswordModal
        email="nuevo@test.com"
        password="Abc123!xyz"
        onClose={vi.fn()}
      />
    );
    expect(screen.getByText("nuevo@test.com")).toBeTruthy();
    expect(screen.getByText("Abc123!xyz")).toBeTruthy();
  });

  it("shows warning about one-time display", () => {
    render(
      <TempPasswordModal
        email="nuevo@test.com"
        password="Abc123!xyz"
        onClose={vi.fn()}
      />
    );
    expect(screen.getByText(/no se mostrará nuevamente/i)).toBeTruthy();
  });

  it("calls onClose when button is clicked", () => {
    const onClose = vi.fn();
    render(
      <TempPasswordModal
        email="nuevo@test.com"
        password="Abc123!xyz"
        onClose={onClose}
      />
    );
    fireEvent.click(screen.getByText("Entendido"));
    expect(onClose).toHaveBeenCalledOnce();
  });
});

// ── UserTable ─────────────────────────────────────────────────────────────────

describe("UserTable", () => {
  const defaultProps = {
    users: [mockUser, mockInactiveUser],
    total: 2,
    page: 1,
    pages: 1,
    roleFilter: "",
    statusFilter: "",
    onRoleFilter: vi.fn(),
    onStatusFilter: vi.fn(),
    onPageChange: vi.fn(),
    onEdit: vi.fn(),
    onToggleStatus: vi.fn(),
    isTogglingId: null,
  };

  it("renders users list", () => {
    render(<UserTable {...defaultProps} />);
    expect(screen.getByText("Juan Lopez")).toBeTruthy();
    expect(screen.getByText("juan@test.com")).toBeTruthy();
  });

  it("shows empty state when no users", () => {
    render(<UserTable {...defaultProps} users={[]} total={0} />);
    expect(screen.getByText(/no hay usuarios/i)).toBeTruthy();
  });

  it("shows deactivate button for active user", () => {
    render(<UserTable {...defaultProps} />);
    expect(screen.getAllByText("Desactivar").length).toBeGreaterThan(0);
  });

  it("shows activate button for inactive user", () => {
    render(<UserTable {...defaultProps} />);
    expect(screen.getByText("Activar")).toBeTruthy();
  });
});
