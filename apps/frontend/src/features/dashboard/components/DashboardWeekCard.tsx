"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import type { CheckInResponse } from "@/features/checkins/services/checkin-service";
import type { CRSCurrentResponse } from "@/features/crs/services/crs-service";
import type { ApiError } from "@/lib/api-client";

interface DashboardWeekCardProps {
  checkInData: CheckInResponse | undefined;
  checkInLoading: boolean;
  checkInError: unknown;
  crsData: CRSCurrentResponse | undefined;
}

function getWeekState(
  checkInData: CheckInResponse | undefined,
  checkInError: unknown,
  crsData: CRSCurrentResponse | undefined,
): "no_checkin" | "draft" | "needs_checkout" | "complete" {
  const is404 = (checkInError as ApiError)?.status === 404;
  if (!checkInData || is404) return "no_checkin";
  if (checkInData.status === "draft") return "draft";
  if (checkInData.status === "submitted") {
    const checkoutDone = crsData?.week_start === checkInData.week_start;
    return checkoutDone ? "complete" : "needs_checkout";
  }
  return "complete";
}

export function DashboardWeekCard({ checkInData, checkInLoading, checkInError, crsData }: DashboardWeekCardProps) {
  if (checkInLoading) {
    return (
      <Card>
        <CardHeader><CardTitle>Esta Semana</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-1/2" />
          <Skeleton className="h-9 w-40" />
        </CardContent>
      </Card>
    );
  }

  const weekState = getWeekState(checkInData, checkInError, crsData);

  const total = checkInData?.priorities?.length ?? 0;
  const completed = checkInData?.priorities?.filter(p => p.status === "completed").length ?? 0;
  const inProgress = checkInData?.priorities?.filter(p => p.status === "in_progress").length ?? 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Esta Semana</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {weekState === "no_checkin" && (
          <>
            <p className="text-sm text-secondary">No has creado tu check-in esta semana.</p>
            <Link
              href="/employee/checkin/new"
              className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90"
            >
              Crear Check-In
            </Link>
          </>
        )}

        {weekState === "draft" && (
          <>
            <div className="flex items-center gap-2">
              <Badge variant="warning">Borrador</Badge>
              {total > 0 && (
                <span className="text-sm text-secondary">{total} prioridad{total !== 1 ? "es" : ""}</span>
              )}
            </div>
            <Link
              href="/employee/checkin"
              className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90"
            >
              Enviar Check-In
            </Link>
          </>
        )}

        {weekState === "needs_checkout" && (
          <>
            <div className="flex items-center gap-2">
              <Badge variant="success">Check-In enviado</Badge>
            </div>
            <div className="text-sm text-secondary space-y-1">
              <p>{total} prioridad{total !== 1 ? "es" : ""} · {completed} completada{completed !== 1 ? "s" : ""} · {inProgress} en progreso</p>
            </div>
            <Link
              href="/employee/checkout"
              className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90"
            >
              Completar Check-Out
            </Link>
          </>
        )}

        {weekState === "complete" && (
          <>
            <Badge variant="success">Semana completada</Badge>
            <p className="text-sm text-secondary">
              {completed}/{total} prioridades completadas
            </p>
          </>
        )}
      </CardContent>
    </Card>
  );
}
