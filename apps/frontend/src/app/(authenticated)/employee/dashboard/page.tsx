"use client";

import Link from "next/link";
import { useDashboardData } from "@/features/dashboard/hooks/useDashboardData";
import { DashboardWeekCard } from "@/features/dashboard/components/DashboardWeekCard";
import { DashboardPrioritiesList } from "@/features/dashboard/components/DashboardPrioritiesList";
import { CRSScoreCard } from "@/features/crs/components/CRSScoreCard";
import { CRSEmptyState } from "@/features/crs/components/CRSEmptyState";
import { CRSHistoryChart } from "@/features/crs/components/CRSHistoryChart";
import { Skeleton } from "@/components/ui/skeleton";
import type { ApiError } from "@/lib/api-client";

export default function EmployeeDashboard() {
  const { checkIn, crs, history } = useDashboardData();

  const crsIs404 = (crs.error as unknown as ApiError)?.status === 404;
  const hasCRS = !!crs.data && !crsIs404;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>

      {/* Row 1: CRS + Week Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section aria-label="Mi CRS">
          {crs.isLoading ? (
            <Skeleton className="h-48 w-full" />
          ) : hasCRS ? (
            <>
              <CRSScoreCard crs={crs.data!} />
              <div className="mt-2 text-right">
                <Link href="/employee/crs" className="text-sm text-primary hover:underline">
                  Ver historial completo →
                </Link>
              </div>
            </>
          ) : (
            <CRSEmptyState />
          )}
        </section>

        <section aria-label="Esta Semana">
          <DashboardWeekCard
            checkInData={checkIn.data}
            checkInLoading={checkIn.isLoading}
            checkInError={checkIn.error}
            crsData={crs.data}
          />
        </section>
      </div>

      {/* Row 2: Active Priorities */}
      {checkIn.data && (
        <section aria-label="Prioridades Activas">
          <DashboardPrioritiesList
            priorities={checkIn.data.priorities}
            checkinId={checkIn.data.id}
          />
        </section>
      )}

      {/* Row 3: CRS History */}
      {history.data && history.data.items.length > 0 && (
        <section aria-label="Historial CRS">
          <CRSHistoryChart items={history.data.items} />
        </section>
      )}
    </div>
  );
}
