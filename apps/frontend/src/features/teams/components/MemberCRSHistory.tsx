"use client";

import { TeamMemberCRSHistoryItem } from "../services/team-service";
import { CRSTrendIndicator } from "@/features/crs/components/CRSTrendIndicator";

interface MemberCRSHistoryProps {
  history: TeamMemberCRSHistoryItem[];
  selectedWeek?: string;
  onSelectWeek?: (week: string) => void;
}

const riskLabels = { low: "Bajo", moderate: "Moderado", high: "Alto" };
const riskColors = {
  low: "text-green-700",
  moderate: "text-orange-700",
  high: "text-red-700",
};

export function MemberCRSHistory({ history, selectedWeek, onSelectWeek }: MemberCRSHistoryProps) {
  if (history.length === 0) {
    return <p className="text-sm text-secondary">Sin historial de CRS disponible.</p>;
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-left text-xs font-medium uppercase text-secondary">
          <tr>
            <th scope="col" className="px-4 py-3">Semana</th>
            <th scope="col" className="px-4 py-3">Score</th>
            <th scope="col" className="px-4 py-3">Tendencia</th>
            <th scope="col" className="px-4 py-3">Riesgo</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border bg-white">
          {history.map((item) => {
            const isSelected = item.week_start === selectedWeek;
            return (
              <tr
                key={item.week_start}
                onClick={() => onSelectWeek?.(item.week_start)}
                className={`transition-colors ${
                  onSelectWeek ? "cursor-pointer" : ""
                } ${
                  isSelected
                    ? "bg-primary/10 ring-1 ring-inset ring-primary/20"
                    : "hover:bg-gray-50"
                }`}
                aria-selected={isSelected}
              >
                <td className="px-4 py-2 font-medium">{item.week_start}</td>
                <td className="px-4 py-2 font-semibold">{item.score.toFixed(1)}</td>
                <td className="px-4 py-2"><CRSTrendIndicator trend={item.trend} /></td>
                <td className={`px-4 py-2 font-medium ${riskColors[item.risk_level]}`}>
                  {riskLabels[item.risk_level]}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
