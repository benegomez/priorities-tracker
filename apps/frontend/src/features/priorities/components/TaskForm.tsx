"use client";

import { useState } from "react";
import { useCreateTask } from "../hooks/useCreateTask";

interface TaskFormProps {
  priorityId: string;
  checkinId: string;
}

export function TaskForm({ priorityId, checkinId }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const { mutate, isPending } = useCreateTask(checkinId);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    mutate(
      { priorityId, data: { title: title.trim() } },
      { onSuccess: () => setTitle("") }
    );
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mt-2">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Nueva tarea..."
        aria-label="Título de la tarea"
        className="flex-1 rounded-md border px-2 py-1 text-sm"
        maxLength={255}
      />
      <button
        type="submit"
        disabled={isPending || !title.trim()}
        className="rounded-md bg-gray-800 px-2 py-1 text-xs text-white disabled:opacity-50"
      >
        {isPending ? "..." : "+"}
      </button>
    </form>
  );
}
