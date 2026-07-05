"use client";

import { useState } from "react";
import { useCurrentCheckIn } from "@/features/checkins/hooks/useCurrentCheckIn";
import { useCurrentCheckOut } from "@/features/checkouts/hooks/useCurrentCheckOut";
import { CheckInForm } from "@/features/checkins/components/CheckInForm";
import { CheckInStatus } from "@/features/checkins/components/CheckInStatus";
import { CheckInLockedBanner } from "@/features/checkins/components/CheckInLockedBanner";
import { CheckInPriorityCard } from "@/features/checkins/components/CheckInPriorityCard";
import { ResubmitButton } from "@/features/checkins/components/ResubmitButton";
import { SubmitCheckInButton } from "@/features/checkins/components/SubmitCheckInButton";
import { PriorityForm } from "@/features/priorities/components/PriorityForm";
import { Badge } from "@/components/ui/badge";
import type { ApiError } from "@/lib/api-client";


export default function CheckInPage() {
  const { data: checkin, isLoading, error } = useCurrentCheckIn();
  const { data: checkout } = useCurrentCheckOut();
  const [showAddForm, setShowAddForm] = useState(false);

  function handlePriorityCreated() {
    setShowAddForm(false);
  }

  if (isLoading) {
    return (
      <div className="space-y-4 animate-pulse" aria-live="polite">
        <div className="h-8 w-48 bg-gray-200 rounded-lg" />
        <div className="h-4 w-64 bg-gray-200 rounded-lg" />
        <div className="h-24 bg-gray-200 rounded-lg" />
      </div>
    );
  }

  const apiError = error as ApiError | null;

  // No check-in exists
  if (apiError?.status === 404 || !checkin) {
    return <CheckInForm />;
  }

  if (apiError) {
    return <p className="text-danger" role="alert">Error: {apiError.message}</p>;
  }

  const isSubmitted = checkin.status === "submitted";
  const isDraft = checkin.status === "draft";
  const isLocked = isSubmitted && !!checkout;
  const isEditable = isSubmitted && !checkout;
  const totalPriorities = checkin.priorities_count ?? 0;
  const newPrioritiesCount = (checkin.priorities ?? []).filter(p => p.status === "draft").length;

  // ─── DRAFT: construction view (original flow) ───────────────────────
  if (isDraft) {
    return (
      <div className="space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Check-In Semanal</h1>
            <p className="text-sm text-secondary">Semana del {checkin.week_start}</p>
          </div>
          <CheckInStatus status={checkin.status} />
        </header>

        {/* Existing priorities from backend */}
        <div className="space-y-3">
          {(checkin.priorities ?? []).map((priority) => (
            <CheckInPriorityCard
              key={priority.id}
              priority={priority}
              checkinId={checkin.id}
              editable={true}
            />
          ))}
        </div>

        <PriorityForm checkinId={checkin.id} onPriorityCreated={handlePriorityCreated} />

        <div className="flex justify-end pt-4 border-t border-border">
          <SubmitCheckInButton checkinId={checkin.id} prioritiesCount={totalPriorities} />
        </div>
      </div>
    );
  }

  // ─── SUBMITTED: detail view (editable or locked) ────────────────────
  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Check-In Semanal</h1>
          <p className="text-sm text-secondary">Semana del {checkin.week_start}</p>
          {checkin.submitted_at && (
            <p className="text-xs text-secondary mt-1">
              Enviado el {new Date(checkin.submitted_at).toLocaleDateString("es", { day: "numeric", month: "short", year: "numeric" })}
            </p>
          )}
        </div>
        {isLocked ? (
          <Badge variant="warning">Bloqueado 🔒</Badge>
        ) : (
          <Badge variant="success">Enviado</Badge>
        )}
      </header>

      {isLocked && <CheckInLockedBanner />}

      {/* Existing priorities from backend */}
      <div className="space-y-3">
        {(checkin.priorities ?? []).map((priority) => (
          <CheckInPriorityCard
            key={priority.id}
            priority={priority}
            checkinId={checkin.id}
            editable={isEditable}
          />
        ))}
      </div>

      {/* Add priority form (expandable) */}
      {isEditable && (
        <div className="space-y-3">
          {showAddForm ? (
            <PriorityForm checkinId={checkin.id} onPriorityCreated={handlePriorityCreated} />
          ) : (
            <button
              onClick={() => setShowAddForm(true)}
              className="w-full rounded-lg border border-dashed border-border p-3 text-sm text-secondary hover:border-primary hover:text-primary transition-colors"
            >
              + Agregar Prioridad
            </button>
          )}
        </div>
      )}

      {/* Re-submit button */}
      {isEditable && (
        <div className="flex justify-end pt-4 border-t border-border">
          <ResubmitButton checkinId={checkin.id} newPrioritiesCount={newPrioritiesCount} />
        </div>
      )}
    </div>
  );
}
