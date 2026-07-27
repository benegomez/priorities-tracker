"use client";

import { TeamMember } from "../services/team-service";
import { TeamCRSBadge } from "./TeamCRSBadge";
import { TeamWeekStatusBadge } from "./TeamWeekStatusBadge";
import { CRSTrendIndicator } from "@/features/crs/components/CRSTrendIndicator";
import { MemberCheckInView } from "./MemberCheckInView";
import { useTeamMemberCheckIn } from "../hooks/useTeamMemberCheckIn";

interface WeeklyMemberRowProps {
  member: TeamMember;
  isExpanded: boolean;
  onToggle: () => void;
}

function ExpandedCheckIn({ employeeId }: { employeeId: string }) {
  const { data, isLoading } = useTeamMemberCheckIn(employeeId);
  if (isLoading) return <p className="text-sm text-secondary px-4 py-3">Cargando...</p>;
  if (!data) return <p className="text-sm text-secondary px-4 py-3">Sin datos de check-in.</p>;
  return (
    <div className="px-4 py-3 bg-gray-50 border-t border-border">
      <MemberCheckInView priorities={data.priorities} weekStart={data.week_start} status={data.status} />
    </div>
  );
}

export function WeeklyMemberRow({ member, isExpanded, onToggle }: WeeklyMemberRowProps) {
  const hasCheckIn = !!member.week_status.checkin_status;

  return (
    <>
      <tr
        className={`border-b border-border transition-colors ${hasCheckIn ? "cursor-pointer hover:bg-gray-50" : "bg-white"}`}
        onClick={hasCheckIn ? onToggle : undefined}
        aria-expanded={hasCheckIn ? isExpanded : undefined}
      >
        <td className="px-4 py-3">
          <div className="flex items-center gap-2">
            {hasCheckIn && (
              <span className="text-xs text-secondary" aria-hidden="true">
                {isExpanded ? "▾" : "▸"}
              </span>
            )}
            <div>
              <p className="font-medium text-gray-900">{member.first_name} {member.last_name}</p>
              <p className="text-xs text-secondary">{member.email}</p>
            </div>
          </div>
        </td>
        <td className="px-4 py-3">
          {member.crs ? (
            <TeamCRSBadge score={member.crs.score} riskLevel={member.crs.risk_level} />
          ) : (
            <span className="text-secondary">—</span>
          )}
        </td>
        <td className="px-4 py-3">
          {member.crs ? (
            <CRSTrendIndicator trend={member.crs.trend} />
          ) : (
            <span className="text-secondary">—</span>
          )}
        </td>
        <td className="px-4 py-3">
          <TeamWeekStatusBadge status={member.week_status.checkin_status} label="Check-In" />
        </td>
        <td className="px-4 py-3">
          <TeamWeekStatusBadge status={member.week_status.checkout_status} label="Check-Out" />
        </td>
      </tr>
      {!hasCheckIn && (
        <tr className="border-b border-border bg-yellow-50">
          <td colSpan={5} className="px-4 py-2">
            <p className="text-xs text-yellow-700" role="alert">
              Sin check-in esta semana
            </p>
          </td>
        </tr>
      )}
      {hasCheckIn && isExpanded && (
        <tr className="border-b border-border">
          <td colSpan={5} className="p-0">
            <ExpandedCheckIn employeeId={member.id} />
          </td>
        </tr>
      )}
    </>
  );
}
