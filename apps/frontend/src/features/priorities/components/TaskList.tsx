"use client";

import type { TaskResponse } from "../services/priority-service";

interface TaskListProps {
  tasks: TaskResponse[];
}

const statusIcon: Record<string, string> = {
  pending: "○",
  in_progress: "◐",
  completed: "●",
  cancelled: "✕",
};

export function TaskList({ tasks }: TaskListProps) {
  if (tasks.length === 0) return null;

  return (
    <ul className="mt-2 space-y-1">
      {tasks.map((task) => (
        <li key={task.id} className="flex items-center gap-2 text-sm text-gray-700">
          <span aria-hidden="true">{statusIcon[task.status]}</span>
          <span>{task.title}</span>
        </li>
      ))}
    </ul>
  );
}
