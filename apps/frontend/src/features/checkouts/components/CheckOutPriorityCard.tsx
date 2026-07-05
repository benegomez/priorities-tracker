"use client";

import { useMarkPriority } from "../hooks/useMarkPriority";
import { useMarkTask } from "../hooks/useMarkTask";
import { useQueryClient } from "@tanstack/react-query";
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
  const markPriority = useMarkPriority();
  const markTask = useMarkTask();
  const queryClient = useQueryClient();

  function handlePriorityToggle() {
    const newCompleted = !priority.completed;
    // Mark priority
    markPriority.mutate({ checkoutId, priorityId: priority.id, completed: newCompleted });
    // Cascade: mark all tasks the same
    if (priority.tasks.length > 0) {
      priority.tasks.forEach((task) => {
        if (task.completed !== newCompleted) {
          markTask.mutate({ checkoutId, taskId: task.id, completed: newCompleted });
        }
      });
    }
  }

  function handleTaskToggle(taskId: string, currentCompleted: boolean) {
    const newTaskCompleted = !currentCompleted;
    markTask.mutate(
      { checkoutId, taskId, completed: newTaskCompleted },
      {
        onSuccess: () => {
          // After marking task, check if all tasks are now completed
          const otherTasks = priority.tasks.filter((t) => t.id !== taskId);
          const allOthersCompleted = otherTasks.every((t) => t.completed);

          if (newTaskCompleted && allOthersCompleted && !priority.completed) {
            // All tasks completed → auto-mark priority
            markPriority.mutate({ checkoutId, priorityId: priority.id, completed: true });
          } else if (!newTaskCompleted && priority.completed) {
            // A task was unchecked → unmark priority
            markPriority.mutate({ checkoutId, priorityId: priority.id, completed: false });
          }
        },
      }
    );
  }

  return (
    <div className="rounded-lg border border-border bg-white p-4">
      <div className="flex items-center gap-3">
        {!readOnly && (
          <input
            type="checkbox"
            checked={priority.completed}
            onChange={handlePriorityToggle}
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
            <div key={task.id} className="flex items-center gap-2 py-1 pl-8">
              {!readOnly && (
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => handleTaskToggle(task.id, task.completed)}
                  className="h-4 w-4 rounded border-border text-primary focus:ring-primary"
                  aria-label={`Marcar tarea "${task.title}" como completada`}
                />
              )}
              <span className={task.completed ? "line-through text-secondary text-sm" : "text-sm"}>
                {task.title}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
