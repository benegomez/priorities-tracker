"use client";

import { useCurrentCRS } from "@/features/crs/hooks/useCurrentCRS";
import { useCRSHistory } from "@/features/crs/hooks/useCRSHistory";
import { CRSScoreCard } from "@/features/crs/components/CRSScoreCard";
import { CRSTrendIndicator } from "@/features/crs/components/CRSTrendIndicator";
import { CRSHistoryChart } from "@/features/crs/components/CRSHistoryChart";
import { CRSEmptyState } from "@/features/crs/components/CRSEmptyState";
import type { ApiError } from "@/lib/api-client";

export default function CRSPage() {
  const { data: crs, isLoading, error } = useCurrentCRS();
  const { data: history } = useCRSHistory();

  if (isLoading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-8 w-32 bg-gray-200 rounded-lg" />
        <div className="h-48 bg-gray-200 rounded-lg" />
        <div className="h-32 bg-gray-200 rounded-lg" />
      </div>
    );
  }

  const apiError = error as ApiError | null;

  if (apiError?.status === 404 || !crs) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-gray-900">Mi CRS</h1>
        <CRSEmptyState />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Mi CRS</h1>
        <CRSTrendIndicator trend={crs.trend} />
      </header>

      <CRSScoreCard crs={crs} />

      {history && history.items.length > 0 && (
        <CRSHistoryChart items={history.items} />
      )}
    </div>
  );
}
