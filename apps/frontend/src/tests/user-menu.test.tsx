import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { UserMenu } from "@/components/layout/UserMenu";
import { useAuthStore } from "@/store/auth-store";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

describe("UserMenu", () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: { id: "u1", email: "test@org.com", role: "employee", organization_id: "o1", full_name: "Juan Pérez" },
      accessToken: "token",
      refreshToken: "refresh",
    });
  });

  it("renders avatar and user name", () => {
    render(<UserMenu />, { wrapper });
    expect(screen.getByText("Juan Pérez")).toBeInTheDocument();
    expect(screen.getByText("JP")).toBeInTheDocument();
  });

  it("opens dropdown on click", () => {
    render(<UserMenu />, { wrapper });
    fireEvent.click(screen.getByLabelText("Menú de usuario"));
    expect(screen.getByRole("menu")).toBeInTheDocument();
  });

  it("shows logout option in dropdown", () => {
    render(<UserMenu />, { wrapper });
    fireEvent.click(screen.getByLabelText("Menú de usuario"));
    expect(screen.getByRole("menuitem", { name: /cerrar sesión/i })).toBeInTheDocument();
  });
});
