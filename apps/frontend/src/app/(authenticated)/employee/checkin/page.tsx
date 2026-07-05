"use client";

import { useState } from "react";
import { useCurrentCheckIn } from "@/features/checkins/hooks/useCurrentCheckIn";
import { CheckInForm } from "@/features/checkins/components/CheckInForm";
import { CheckInStatus } from "@/features/checkins/components/CheckInStatus";
import { SubmitCheckInButton } from "@/features/checkins/components/SubmitCheckInButton";
import { PriorityList } from "@/features/priorities/components/PriorityList";
import { PriorityForm } from "@/features/priorities/components/PriorityForm";
import type { ApiError } from "@/lib/api-client";
import type { PriorityResponse } from "@/features/priorities/services/priority-service";

// TODO: Fetch from API when projects module has list endpoint
const MOCK_PHASES = [
  { id: "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", name: "Descubrimiento", project_name: "Proyecto Alpha" },
  { id: "cccccccc-cccc-cccc-cccc-cccccccccccc", name: "Desarrollo", project_name: "Proyecto Alpha" },
  { id: "dddddddd-dddd-dddd-dddd-dddddddddddd", name: "Pruebas", project_name: "Proyecto Alpha" },
];

export default function CheckInPage() {
  const { data: checkin, isLoading, error } = useCurrentCheckIn();
  const [priorities, setPriorities] = useState<PriorityResponse[]>([]);

  function handlePriorityCreated(priority: PriorityResponse) {
    setPriorities((prev) => [...prev, { ...priority, tasks: priority.tasks ?? [] }]);
  }

  function handleTaskCreated(priorityId: string, task: { id: string; priority_id: string; title: string; description: string | null; status: "pending" | "in_progress" | "completed" | "cancelled"; created_at: string; updated_at: string }) {
    setPriorities((prev) =>
      prev.map((p) =>
        p.id === priorityId ? { ...p, tasks: [...p.tasks, task] } : p
      )
    );
  }

  if (isLoading) {
    return (
      <div className="p-8" aria-live="polite">
        <div className="animate-pulse space-y-4">
          <div className="h-8 w-48 bg-gray-200 rounded" />
          <div className="h-4 w-64 bg-gray-200 rounded" />
        </div>
      </div>
    );
  }

  const apiError = error as ApiError | null;

  // No check-in exists for this week
  if (apiError?.status === 404 || !checkin) {
    return <CheckInForm />;
  }

  // Unexpected error
  if (apiError) {
    return (
      <div className="p-8">
        <p className="text-red-600" role="alert">Error: {apiError.message}</p>
      </div>
    );
  }

  const isReadOnly = checkin.status !== "draft";
  const totalPriorities = (checkin.priorities_count ?? 0) + priorities.length;

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Check-In Semanal</h1>
          <p className="text-gray-600 text-sm">Semana del {checkin.week_start}</p>
        </div>
        <CheckInStatus status={checkin.status} />
      </header>

      <PriorityList priorities={priorities} checkinId={checkin.id} readOnly={isReadOnly} onTaskCreated={handleTaskCreated} />

      {!isReadOnly && (
        <>
          <PriorityForm checkinId={checkin.id} phases={MOCK_PHASES} onPriorityCreated={handlePriorityCreated} />
          <div className="flex justify-end pt-4 border-t">
            <SubmitCheckInButton checkinId={checkin.id} prioritiesCount={totalPriorities} />
          </div>
        </>
      )}

      {isReadOnly && (
        <div className="rounded-lg bg-green-50 p-4 text-center">
          <p className="text-green-800 font-medium">✓ Check-In enviado exitosamente</p>
          {checkin.submitted_at && (
            <p className="text-green-600 text-sm mt-1">
              Enviado el {new Date(checkin.submitted_at).toLocaleDateString("es")}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
