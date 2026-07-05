"use client";

import { useState } from "react";
import { useCurrentCheckOut } from "@/features/checkouts/hooks/useCurrentCheckOut";
import { CheckOutForm } from "@/features/checkouts/components/CheckOutForm";
import { CheckOutPriorityCard } from "@/features/checkouts/components/CheckOutPriorityCard";
import { CheckOutNotes } from "@/features/checkouts/components/CheckOutNotes";
import { CheckOutSummaryCard } from "@/features/checkouts/components/CheckOutSummary";
import { SubmitCheckOutButton } from "@/features/checkouts/components/SubmitCheckOutButton";
import { Badge } from "@/components/ui/badge";
import type { ApiError } from "@/lib/api-client";

export default function CheckOutPage() {
  const { data: checkout, isLoading, error } = useCurrentCheckOut();
  const [notes, setNotes] = useState("");
  const [lessonsLearned, setLessonsLearned] = useState("");

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

  if (apiError?.status === 404 || !checkout) {
    return <CheckOutForm />;
  }

  if (apiError) {
    return <p className="text-danger" role="alert">Error: {apiError.message}</p>;
  }

  const isReadOnly = checkout.status !== "draft";

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Check-Out Semanal</h1>
          <p className="text-sm text-secondary">Semana del {checkout.week_start}</p>
        </div>
        <Badge variant={isReadOnly ? "success" : "default"}>
          {isReadOnly ? "Enviado" : "Borrador"}
        </Badge>
      </header>

      {isReadOnly ? (
        <CheckOutSummaryCard submittedAt={checkout.submitted_at} summary={{
          priorities_total: checkout.priorities.length,
          priorities_completed: checkout.priorities.filter(p => p.completed).length,
          priorities_carried: checkout.priorities.filter(p => !p.completed).length,
          tasks_total: checkout.priorities.reduce((sum, p) => sum + p.tasks.length, 0),
          tasks_completed: checkout.priorities.reduce((sum, p) => sum + p.tasks.filter(t => t.completed).length, 0),
        }} />
      ) : (
        <>
          <div className="space-y-3">
            <h2 className="text-sm font-medium text-secondary uppercase tracking-wider">
              Marca las prioridades que completaste
            </h2>
            {checkout.priorities.length === 0 ? (
              <p className="text-secondary text-sm">No hay prioridades registradas.</p>
            ) : (
              checkout.priorities.map((priority) => (
                <CheckOutPriorityCard
                  key={priority.id}
                  checkoutId={checkout.id}
                  priority={priority}
                  readOnly={isReadOnly}
                />
              ))
            )}
          </div>

          <CheckOutNotes
            notes={notes}
            lessonsLearned={lessonsLearned}
            onNotesChange={setNotes}
            onLessonsChange={setLessonsLearned}
            readOnly={isReadOnly}
          />

          <div className="flex justify-end pt-4 border-t border-border">
            <SubmitCheckOutButton checkoutId={checkout.id} notes={notes} lessonsLearned={lessonsLearned} />
          </div>
        </>
      )}
    </div>
  );
}
