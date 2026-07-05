"use client";

import { useCreateCheckIn } from "../hooks/useCreateCheckIn";
import type { ApiError } from "@/lib/api-client";

function getCurrentWeekStart(): string {
  const now = new Date();
  // In development, use today's date to allow testing any day
  // In production, always calculate the Monday of the current week
  if (process.env.NODE_ENV === "development") {
    return now.toISOString().split("T")[0];
  }
  const day = now.getDay();
  const diff = day === 0 ? -6 : 1 - day;
  const monday = new Date(now);
  monday.setDate(now.getDate() + diff);
  return monday.toISOString().split("T")[0];
}

export function CheckInForm() {
  const { mutate, isPending, error } = useCreateCheckIn();

  function handleCreate() {
    mutate(getCurrentWeekStart());
  }

  const apiError = error as ApiError | null;

  return (
    <div className="flex flex-col items-center gap-4 p-8">
      <h2 className="text-xl font-semibold">No tienes un Check-In para esta semana</h2>
      <p className="text-gray-600">Crea tu Check-In semanal para registrar tus compromisos.</p>
      <button
        onClick={handleCreate}
        disabled={isPending}
        className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        aria-label="Crear Check-In semanal"
      >
        {isPending ? "Creando..." : "Crear Check-In"}
      </button>
      {apiError && (
        <p className="text-sm text-red-600" role="alert" aria-live="polite">
          {apiError.message}
        </p>
      )}
    </div>
  );
}
