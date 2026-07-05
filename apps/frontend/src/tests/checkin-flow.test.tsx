import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { CheckInForm } from "@/features/checkins/components/CheckInForm";
import { CheckInStatus } from "@/features/checkins/components/CheckInStatus";
import { SubmitCheckInButton } from "@/features/checkins/components/SubmitCheckInButton";
import { PriorityCard } from "@/features/priorities/components/PriorityCard";
import { PriorityList } from "@/features/priorities/components/PriorityList";
import { TaskForm } from "@/features/priorities/components/TaskForm";
import { TaskList } from "@/features/priorities/components/TaskList";
import type { PriorityResponse, TaskResponse } from "@/features/priorities/services/priority-service";

// Mock next/navigation
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

const mockPriority: PriorityResponse = {
  id: "p1",
  checkin_id: "c1",
  phase_id: "ph1",
  owner_id: "u1",
  organization_id: "o1",
  title: "Implementar login",
  description: "Flujo completo de autenticación",
  priority_level: "high",
  status: "draft",
  week_start: "2025-01-06",
  created_at: "2025-01-06T00:00:00Z",
  updated_at: "2025-01-06T00:00:00Z",
  tasks: [
    { id: "t1", priority_id: "p1", title: "Crear endpoint", description: null, status: "pending", created_at: "2025-01-06T00:00:00Z", updated_at: "2025-01-06T00:00:00Z" },
    { id: "t2", priority_id: "p1", title: "Agregar tests", description: null, status: "completed", created_at: "2025-01-06T00:00:00Z", updated_at: "2025-01-06T00:00:00Z" },
  ],
};

describe("CheckInForm", () => {
  it("renders create button", () => {
    render(<CheckInForm />, { wrapper });
    expect(screen.getByRole("button", { name: /crear check-in/i })).toBeInTheDocument();
  });

  it("shows loading state when clicked", async () => {
    // Mock fetch to delay
    global.fetch = vi.fn(() => new Promise(() => {})) as unknown as typeof fetch;
    render(<CheckInForm />, { wrapper });
    fireEvent.click(screen.getByRole("button", { name: /crear check-in/i }));
    await waitFor(() => {
      expect(screen.getByText("Creando...")).toBeInTheDocument();
    });
  });
});

describe("CheckInStatus", () => {
  it("renders draft badge", () => {
    render(<CheckInStatus status="draft" />);
    expect(screen.getByText("Borrador")).toBeInTheDocument();
  });

  it("renders submitted badge", () => {
    render(<CheckInStatus status="submitted" />);
    expect(screen.getByText("Enviado")).toBeInTheDocument();
  });
});

describe("SubmitCheckInButton", () => {
  it("is disabled when no priorities", () => {
    render(<SubmitCheckInButton checkinId="c1" prioritiesCount={0} />, { wrapper });
    expect(screen.getByRole("button", { name: /enviar check-in/i })).toBeDisabled();
  });

  it("is enabled with priorities", () => {
    render(<SubmitCheckInButton checkinId="c1" prioritiesCount={2} />, { wrapper });
    expect(screen.getByRole("button", { name: /enviar check-in/i })).not.toBeDisabled();
  });

  it("shows confirmation dialog on click", async () => {
    render(<SubmitCheckInButton checkinId="c1" prioritiesCount={2} />, { wrapper });
    fireEvent.click(screen.getByRole("button", { name: /enviar check-in/i }));
    await waitFor(() => {
      expect(screen.getByText("Confirmar envío")).toBeInTheDocument();
    });
  });

  it("shows helper text when disabled", () => {
    render(<SubmitCheckInButton checkinId="c1" prioritiesCount={0} />, { wrapper });
    expect(screen.getByText(/agrega al menos una prioridad/i)).toBeInTheDocument();
  });
});

describe("PriorityCard", () => {
  it("renders title, level, and task count", () => {
    render(<PriorityCard priority={mockPriority} checkinId="c1" />, { wrapper });
    expect(screen.getByText("Implementar login")).toBeInTheDocument();
    expect(screen.getByText("high")).toBeInTheDocument();
    expect(screen.getByText("2 tarea(s)")).toBeInTheDocument();
  });

  it("renders description when present", () => {
    render(<PriorityCard priority={mockPriority} checkinId="c1" />, { wrapper });
    expect(screen.getByText("Flujo completo de autenticación")).toBeInTheDocument();
  });

  it("hides task form in read-only mode", () => {
    render(<PriorityCard priority={mockPriority} checkinId="c1" readOnly />, { wrapper });
    expect(screen.queryByPlaceholderText("Nueva tarea...")).not.toBeInTheDocument();
  });
});

describe("PriorityList", () => {
  it("shows empty message when no priorities", () => {
    render(<PriorityList priorities={[]} checkinId="c1" />, { wrapper });
    expect(screen.getByText(/no hay prioridades/i)).toBeInTheDocument();
  });

  it("renders priority cards", () => {
    render(<PriorityList priorities={[mockPriority]} checkinId="c1" />, { wrapper });
    expect(screen.getByText("Implementar login")).toBeInTheDocument();
  });
});

describe("TaskForm", () => {
  beforeEach(() => {
    global.fetch = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ id: "t3", title: "New", status: "pending" }) })
    ) as unknown as typeof fetch;
  });

  it("renders input and button", () => {
    render(<TaskForm priorityId="p1" checkinId="c1" />, { wrapper });
    expect(screen.getByPlaceholderText("Nueva tarea...")).toBeInTheDocument();
  });

  it("button is disabled with empty input", () => {
    render(<TaskForm priorityId="p1" checkinId="c1" />, { wrapper });
    const btn = screen.getByRole("button", { name: "+" });
    expect(btn).toBeDisabled();
  });

  it("submits with valid title", async () => {
    render(<TaskForm priorityId="p1" checkinId="c1" />, { wrapper });
    const input = screen.getByPlaceholderText("Nueva tarea...");
    fireEvent.change(input, { target: { value: "Nueva tarea" } });
    fireEvent.submit(input.closest("form")!);
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled();
    });
  });
});

describe("TaskList", () => {
  it("renders nothing when empty", () => {
    const { container } = render(<TaskList tasks={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it("renders task titles", () => {
    const tasks: TaskResponse[] = [
      { id: "t1", priority_id: "p1", title: "Task A", description: null, status: "pending", created_at: "", updated_at: "" },
    ];
    render(<TaskList tasks={tasks} />);
    expect(screen.getByText("Task A")).toBeInTheDocument();
  });
});
