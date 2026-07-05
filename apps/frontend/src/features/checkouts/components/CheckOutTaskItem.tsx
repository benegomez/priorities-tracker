"use client";

import { useMarkTask } from "../hooks/useMarkTask";
import type { CheckOutTaskItem as TaskItemType } from "../services/checkout-service";

interface CheckOutTaskItemProps {
  checkoutId: string;
  task: TaskItemType;
  readOnly?: boolean;
}

export function CheckOutTaskItem({ checkoutId, task, readOnly = false }: CheckOutTaskItemProps) {
  const { mutate } = useMarkTask();

  function handleToggle() {
    mutate({ checkoutId, taskId: task.id, completed: !task.completed });
  }

  return (
    <div className="flex items-center gap-2 py-1 pl-8">
      {!readOnly && (
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          className="h-4 w-4 rounded border-border text-primary focus:ring-primary"
          aria-label={`Marcar tarea "${task.title}" como completada`}
        />
      )}
      <span className={task.completed ? "line-through text-secondary text-sm" : "text-sm"}>
        {task.title}
      </span>
    </div>
  );
}
