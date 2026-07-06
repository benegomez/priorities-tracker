"use client";

import Link from "next/link";
import { TeamMember } from "../services/team-service";
import { TeamCRSBadge } from "./TeamCRSBadge";
import { TeamWeekStatusBadge } from "./TeamWeekStatusBadge";
import { CRSTrendIndicator } from "@/features/crs/components/CRSTrendIndicator";

interface TeamTableProps {
  members: TeamMember[];
}

export function TeamTable({ members }: TeamTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-left text-xs font-medium uppercase text-secondary">
          <tr>
            <th scope="col" className="px-4 py-3">Nombre</th>
            <th scope="col" className="px-4 py-3">CRS</th>
            <th scope="col" className="px-4 py-3">Tendencia</th>
            <th scope="col" className="px-4 py-3">Check-In</th>
            <th scope="col" className="px-4 py-3">Check-Out</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border bg-white">
          {members.map((member) => (
            <tr key={member.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-4 py-3">
                <Link href={`/manager/team/${member.id}`} className="font-medium text-primary hover:underline">
                  {member.first_name} {member.last_name}
                </Link>
                <p className="text-xs text-secondary">{member.email}</p>
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
          ))}
        </tbody>
      </table>
    </div>
  );
}
