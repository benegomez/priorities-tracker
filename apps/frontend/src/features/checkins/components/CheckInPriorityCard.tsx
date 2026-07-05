"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { TaskForm } from "@/features/priorities/components/TaskForm";

interface TaskItem {
  id: string;
  title: string;
  status: string;
}

interface CheckInPriorityCardProps {
  priority: {
    id: string;
    title: string;
    description?: string | null;
    priority_level: string;
    status: string;
    phase_name?: string | null;
    project_name?: string | null;
    tasks: TaskItem[];
  };
  checkinId: string;
  editable: boolean;
  onTaskCreated?: (task: TaskItem) => void;
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

export function CheckInPriorityCard({ priority, checkinId, editable, onTaskCreated }: CheckInPriorityCardProps) {
  const isNew = priority.status === "draft";

  return (
    <div className="rounded-lg border border-border bg-white p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="font-medium">{priority.title}</span>
          {isNew && (
            <Badge variant="warning" aria-label="Prioridad nueva">Nueva</Badge>
          )}
        </div>
        <div className="flex gap-2">
          <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${levelColors[priority.priority_level] ?? ""}`}>
            {priority.priority_level}
          </span>
          <Badge variant="outline">{priority.status}</Badge>
        </div>
      </div>

      {/* Project / Phase */}
      {(priority.project_name || priority.phase_name) && (
        <p className="mt-1 text-xs text-secondary">
          {priority.project_name}{priority.phase_name ? ` → ${priority.phase_name}` : ""}
        </p>
      )}

      {/* Description */}
      {priority.description && (
        <p className="mt-1 text-sm text-secondary">{priority.description}</p>
      )}

      {/* Tasks */}
      {priority.tasks.length > 0 && (
        <ul className="mt-2 space-y-1">
          {priority.tasks.map((task) => (
            <li key={task.id} className="flex items-center gap-2 text-sm text-gray-700 pl-1">
              <span aria-hidden="true">{statusIcon[task.status] ?? "○"}</span>
              <span>{task.title}</span>
            </li>
          ))}
        </ul>
      )}

      {/* Add task inline */}
      {editable && (
        <TaskForm priorityId={priority.id} checkinId={checkinId} onTaskCreated={onTaskCreated as any} />
      )}
    </div>
  );
}
