"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { useTeamMemberCRS } from "@/features/teams/hooks/useTeamMemberCRS";
import { useTeamMemberCheckIn } from "@/features/teams/hooks/useTeamMemberCheckIn";
import { MemberCRSHistory } from "@/features/teams/components/MemberCRSHistory";
import { MemberCheckInView } from "@/features/teams/components/MemberCheckInView";
import { TeamCRSBadge } from "@/features/teams/components/TeamCRSBadge";
import { CRSTrendIndicator } from "@/features/crs/components/CRSTrendIndicator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function TeamMemberDetailPage() {
  const params = useParams();
  const employeeId = params.employeeId as string;

  const [selectedWeek, setSelectedWeek] = useState<string | undefined>();

  const { data: crsData, isLoading: crsLoading } = useTeamMemberCRS(employeeId);
  const { data: checkinData, isLoading: checkinLoading, error: checkinError } =
    useTeamMemberCheckIn(employeeId, selectedWeek);

  // Initialize selectedWeek with the most recent week from CRS history
  useEffect(() => {
    if (!selectedWeek && crsData?.history?.length) {
      setSelectedWeek(crsData.history[0].week_start);
    }
  }, [crsData, selectedWeek]);

  const employeeName = crsData
    ? `${crsData.employee.first_name} ${crsData.employee.last_name}`
    : "Cargando...";

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/manager/team" className="text-sm text-primary hover:underline">
          ← Volver al equipo
        </Link>
      </div>

      <h1 className="text-2xl font-semibold text-gray-900">{employeeName}</h1>

      {/* CRS Section */}
      <Card>
        <CardHeader><CardTitle>Commitment Reliability Score</CardTitle></CardHeader>
        <CardContent>
          {crsLoading ? (
            <Skeleton className="h-32 w-full" />
          ) : crsData?.current ? (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <TeamCRSBadge score={crsData.current.score} riskLevel={crsData.current.risk_level} />
                <CRSTrendIndicator trend={crsData.current.trend} />
                <span className="text-sm text-secondary">Semana: {crsData.current.week_start}</span>
              </div>
              <MemberCRSHistory
                history={crsData.history}
                selectedWeek={selectedWeek}
                onSelectWeek={setSelectedWeek}
              />
            </div>
          ) : (
            <p className="text-sm text-secondary">Aún no tiene CRS calculado.</p>
          )}
        </CardContent>
      </Card>

      {/* Check-In Section */}
      <Card>
        <CardHeader>
          <CardTitle>
            Check-In{selectedWeek ? ` — ${selectedWeek}` : " de la Semana"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {checkinLoading ? (
            <Skeleton className="h-32 w-full" aria-label="Cargando check-in" />
          ) : checkinError ? (
            <p className="text-sm text-secondary">No hay check-in registrado para esta semana.</p>
          ) : checkinData ? (
            <MemberCheckInView
              priorities={checkinData.priorities}
              weekStart={checkinData.week_start}
              status={checkinData.status}
            />
          ) : null}
        </CardContent>
      </Card>
    </div>
  );
}
