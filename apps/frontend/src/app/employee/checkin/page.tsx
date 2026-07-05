"use client";

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
  { id: "44444444-4444-4444-4444-444444444444", name: "Fase 1 - Descubrimiento", project_name: "Proyecto Demo" },
];

export default function CheckInPage() {
  const { data: checkin, isLoading, error } = useCurrentCheckIn();

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
  // Priorities come embedded in the check-in response from the current endpoint
  const priorities: PriorityResponse[] = (checkin as unknown as { priorities?: PriorityResponse[] }).priorities ?? [];

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Check-In Semanal</h1>
          <p className="text-gray-600 text-sm">Semana del {checkin.week_start}</p>
        </div>
        <CheckInStatus status={checkin.status} />
      </header>

      <PriorityList priorities={priorities} checkinId={checkin.id} readOnly={isReadOnly} />

      {!isReadOnly && (
        <>
          <PriorityForm checkinId={checkin.id} phases={MOCK_PHASES} />
          <div className="flex justify-end pt-4 border-t">
            <SubmitCheckInButton checkinId={checkin.id} prioritiesCount={checkin.priorities_count} />
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
