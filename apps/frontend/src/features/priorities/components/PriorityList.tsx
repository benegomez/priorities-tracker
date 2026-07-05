"use client";

import type { PriorityResponse } from "../services/priority-service";
import { PriorityCard } from "./PriorityCard";

interface PriorityListProps {
  priorities: PriorityResponse[];
  checkinId: string;
  readOnly?: boolean;
}

export function PriorityList({ priorities, checkinId, readOnly = false }: PriorityListProps) {
  if (priorities.length === 0) {
    return <p className="text-gray-500 text-sm py-4">No hay prioridades aún. Agrega tu primera prioridad.</p>;
  }

  return (
    <div className="space-y-3">
      {priorities.map((priority) => (
        <PriorityCard
          key={priority.id}
          priority={priority}
          checkinId={checkinId}
          readOnly={readOnly}
        />
      ))}
    </div>
  );
}
