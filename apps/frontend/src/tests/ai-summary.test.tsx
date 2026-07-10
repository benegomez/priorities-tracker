import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AISummaryCard } from "@/features/ai/components/AISummaryCard";
import { AISummaryEmptyState } from "@/features/ai/components/AISummaryEmptyState";
import type { TeamSummaryResponse } from "@/features/ai/services/ai-service";

function wrapper({ children }: { children: React.ReactNode }) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

const mockAIResponse: TeamSummaryResponse = {
  summary: "El equipo completó el 72% de sus compromisos esta semana.",
  generated_at: "2026-07-08T10:30:00Z",
  model: "gpt-4o-mini",
  data_snapshot: {
    team_size: 4,
    week_start: "2026-07-08",
    avg_crs: 66.5,
    total_priorities: 13,
    completed_priorities: 9,
    completion_rate: 69.2,
  },
  fallback: false,
  cached: false,
};

const mockCachedResponse: TeamSummaryResponse = {
  ...mockAIResponse,
  cached: true,
};

const mockFallbackResponse: TeamSummaryResponse = {
  ...mockAIResponse,
  summary: "Resumen automático: El equipo completó 9 de 13 prioridades.",
  model: null,
  fallback: true,
  cached: false,
};

describe("AISummaryCard", () => {
  const onRegenerate = vi.fn();

  it("renders summary text", () => {
    render(<AISummaryCard data={mockAIResponse} onRegenerate={onRegenerate} isRegenerating={false} />, { wrapper });
    expect(screen.getByText(/el equipo completó el 72%/i)).toBeInTheDocument();
  });

  it("shows AI badge when fresh (not fallback, not cached)", () => {
    render(<AISummaryCard data={mockAIResponse} onRegenerate={onRegenerate} isRegenerating={false} />, { wrapper });
    expect(screen.getByText("Generado por IA")).toBeInTheDocument();
  });

  it("shows cache badge when cached", () => {
    render(<AISummaryCard data={mockCachedResponse} onRegenerate={onRegenerate} isRegenerating={false} />, { wrapper });
    expect(screen.getByText("Desde cache")).toBeInTheDocument();
  });

  it("shows fallback badge when fallback", () => {
    render(<AISummaryCard data={mockFallbackResponse} onRegenerate={onRegenerate} isRegenerating={false} />, { wrapper });
    expect(screen.getByText("Resumen automático (sin IA)")).toBeInTheDocument();
  });

  it("shows metrics from data_snapshot", () => {
    render(<AISummaryCard data={mockAIResponse} onRegenerate={onRegenerate} isRegenerating={false} />, { wrapper });
    expect(screen.getByText("4")).toBeInTheDocument(); // team_size
    expect(screen.getByText("66.5")).toBeInTheDocument(); // avg_crs
    expect(screen.getByText("69%")).toBeInTheDocument(); // completion_rate
    expect(screen.getByText("9/13")).toBeInTheDocument(); // priorities
  });

  it("shows regenerate button", () => {
    render(<AISummaryCard data={mockAIResponse} onRegenerate={onRegenerate} isRegenerating={false} />, { wrapper });
    const btn = screen.getByText("Regenerar");
    fireEvent.click(btn);
    expect(onRegenerate).toHaveBeenCalled();
  });
});

describe("AISummaryEmptyState", () => {
  it("shows generate button", () => {
    const onGenerate = vi.fn();
    render(<AISummaryEmptyState onGenerate={onGenerate} isLoading={false} />, { wrapper });
    const btn = screen.getByRole("button", { name: /generar resumen/i });
    expect(btn).toBeInTheDocument();
    fireEvent.click(btn);
    expect(onGenerate).toHaveBeenCalled();
  });

  it("shows loading state", () => {
    render(<AISummaryEmptyState onGenerate={vi.fn()} isLoading={true} />, { wrapper });
    expect(screen.getByText(/generando resumen/i)).toBeInTheDocument();
  });
});
