"use client";

import { Badge } from "@/components/ui/badge";
import { CheckInPriority } from "../services/team-service";

interface MemberCheckInViewProps {
  priorities: CheckInPriority[];
  weekStart: string;
  status: string;
}

const levelColors: Record<string, string> = {
  high: "bg-red-100 text-red-800",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-blue-100 text-blue-800",
};

const statusIcon: Record<string, string> = {
  pending: "○",
  in_progress: "◐",
  completed: "●",
  cancelled: "✕",
  draft: "◇",
  planned: "◆",
};

export function MemberCheckInView({ priorities, weekStart, status }: MemberCheckInViewProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-sm text-secondary">Semana: {weekStart}</span>
        <Badge variant="outline">{status}</Badge>
      </div>
      {priorities.length === 0 ? (
        <p className="text-sm text-secondary">Sin prioridades registradas.</p>
      ) : (
        priorities.map((p) => (
          <div key={p.id} className="rounded-lg border border-border bg-white p-4">
            <div className="flex items-center justify-between">
              <span className="font-medium">{p.title}</span>
              <div className="flex gap-2">
                <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${levelColors[p.priority_level] ?? ""}`}>
                  {p.priority_level}
                </span>
                <Badge variant="outline">{p.status}</Badge>
              </div>
            </div>
            {(p.project_name || p.phase_name) && (
              <p className="mt-1 text-xs text-secondary">
                {p.project_name}{p.phase_name ? ` → ${p.phase_name}` : ""}
              </p>
            )}
            {p.description && <p className="mt-1 text-sm text-secondary">{p.description}</p>}
            {p.tasks.length > 0 && (
              <ul className="mt-2 space-y-1">
                {p.tasks.map((t) => (
                  <li key={t.id} className="flex items-center gap-2 text-sm text-gray-700 pl-1">
                    <span aria-hidden="true">{statusIcon[t.status] ?? "○"}</span>
                    <span>{t.title}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))
      )}
    </div>
  );
}
