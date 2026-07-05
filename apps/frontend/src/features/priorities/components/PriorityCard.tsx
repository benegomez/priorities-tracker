"use client";

import type { PriorityResponse, TaskResponse } from "../services/priority-service";
import { TaskList } from "./TaskList";
import { TaskForm } from "./TaskForm";

interface PriorityCardProps {
  priority: PriorityResponse;
  checkinId: string;
  readOnly?: boolean;
  onTaskCreated?: (priorityId: string, task: TaskResponse) => void;
}

const levelColors = {
  high: "bg-red-100 text-red-800",
  medium: "bg-yellow-100 text-yellow-800",
  low: "bg-blue-100 text-blue-800",
};

export function PriorityCard({ priority, checkinId, readOnly = false, onTaskCreated }: PriorityCardProps) {
  return (
    <div className="rounded-lg border p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h4 className="font-medium">{priority.title}</h4>
        <div className="flex gap-2">
          <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${levelColors[priority.priority_level]}`}>
            {priority.priority_level}
          </span>
          <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-700">
            {priority.tasks.length} tarea(s)
          </span>
        </div>
      </div>
      {priority.description && (
        <p className="mt-1 text-sm text-gray-600">{priority.description}</p>
      )}
      <TaskList tasks={priority.tasks} />
      {!readOnly && <TaskForm priorityId={priority.id} checkinId={checkinId} onTaskCreated={(task) => onTaskCreated?.(priority.id, task)} />}
    </div>
  );
}
