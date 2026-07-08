"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckInPriorityCard } from "@/features/checkins/components/CheckInPriorityCard";
import type { CheckInPriorityItem } from "@/features/checkins/services/checkin-service";

interface DashboardPrioritiesListProps {
  priorities: CheckInPriorityItem[];
  checkinId: string;
}

export function DashboardPrioritiesList({ priorities, checkinId }: DashboardPrioritiesListProps) {
  const total = priorities.length;
  const completed = priorities.filter(p => p.status === "completed").length;
  const inProgress = priorities.filter(p => p.status === "in_progress").length;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Prioridades Activas</CardTitle>
          {total > 0 && (
            <span className="text-sm text-secondary">
              {completed}/{total} completadas · {inProgress} en progreso
            </span>
          )}
        </div>
      </CardHeader>
      <CardContent>
        {total === 0 ? (
          <p className="text-sm text-secondary">No hay prioridades registradas esta semana.</p>
        ) : (
          <div className="space-y-3">
            {priorities.map(priority => (
              <CheckInPriorityCard
                key={priority.id}
                priority={priority}
                checkinId={checkinId}
                editable={false}
              />
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
