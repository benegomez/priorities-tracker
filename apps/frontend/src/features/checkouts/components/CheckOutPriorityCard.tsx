"use client";

import { useMarkPriority } from "../hooks/useMarkPriority";
import { CheckOutTaskItem } from "./CheckOutTaskItem";
import type { CheckOutPriorityItem } from "../services/checkout-service";

interface CheckOutPriorityCardProps {
  checkoutId: string;
  priority: CheckOutPriorityItem;
  readOnly?: boolean;
}

const levelColors: Record<string, string> = {
  high: "bg-red-100 text-red-800",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-blue-100 text-blue-800",
};

export function CheckOutPriorityCard({ checkoutId, priority, readOnly = false }: CheckOutPriorityCardProps) {
  const { mutate } = useMarkPriority();

  function handleToggle() {
    mutate({ checkoutId, priorityId: priority.id, completed: !priority.completed });
  }

  return (
    <div className="rounded-lg border border-border bg-white p-4">
      <div className="flex items-center gap-3">
        {!readOnly && (
          <input
            type="checkbox"
            checked={priority.completed}
            onChange={handleToggle}
            className="h-5 w-5 rounded border-border text-primary focus:ring-primary"
            aria-label={`Marcar "${priority.title}" como completada`}
          />
        )}
        <div className="flex-1">
          <span className={priority.completed ? "line-through text-secondary" : "font-medium"}>
            {priority.title}
          </span>
        </div>
        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${levelColors[priority.priority_level] ?? ""}`}>
          {priority.priority_level}
        </span>
      </div>

      {/* Tasks */}
      {priority.tasks.length > 0 && (
        <div className="mt-2 border-t border-border pt-2">
          {priority.tasks.map((task) => (
            <CheckOutTaskItem
              key={task.id}
              checkoutId={checkoutId}
              task={task}
              readOnly={readOnly}
            />
          ))}
        </div>
      )}
    </div>
  );
}
