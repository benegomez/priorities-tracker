"use client";

import { useTeamSummary } from "@/features/ai/hooks/useTeamSummary";
import { AISummaryCard } from "@/features/ai/components/AISummaryCard";
import { AISummaryEmptyState } from "@/features/ai/components/AISummaryEmptyState";

export default function AISummaryPage() {
  const { mutate, data, isPending, error } = useTeamSummary();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Resumen Semanal IA</h1>

      {/* Error state */}
      {error && !data && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
          <p>Error al generar el resumen. Intenta nuevamente.</p>
          <button
            onClick={() => mutate(false)}
            className="mt-2 text-sm font-medium text-primary hover:underline"
          >
            Reintentar
          </button>
        </div>
      )}

      {/* Empty state (before first generation) */}
      {!data && !error && (
        <AISummaryEmptyState onGenerate={() => mutate(false)} isLoading={isPending} />
      )}

      {/* Result */}
      {data && (
        <AISummaryCard
          data={data}
          onRegenerate={() => mutate(true)}
          isRegenerating={isPending}
        />
      )}
    </div>
  );
}
