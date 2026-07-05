"use client";

import type { CheckOutSummary } from "../services/checkout-service";

interface CheckOutSummaryCardProps {
  summary?: CheckOutSummary;
  submittedAt?: string | null;
}

export function CheckOutSummaryCard({ summary, submittedAt }: CheckOutSummaryCardProps) {
  if (!summary) return null;

  return (
    <div className="rounded-lg border border-border bg-green-50 p-6 space-y-3">
      <p className="text-green-800 font-medium text-center">✓ Check-Out enviado exitosamente</p>
      {submittedAt && (
        <p className="text-green-600 text-sm text-center">
          Enviado el {new Date(submittedAt).toLocaleDateString("es")}
        </p>
      )}
      <div className="grid grid-cols-2 gap-4 pt-2">
        <div className="text-center">
          <p className="text-2xl font-semibold text-gray-900">{summary.priorities_completed}/{summary.priorities_total}</p>
          <p className="text-xs text-secondary">Prioridades completadas</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-semibold text-gray-900">{summary.tasks_completed}/{summary.tasks_total}</p>
          <p className="text-xs text-secondary">Tareas completadas</p>
        </div>
      </div>
      {summary.priorities_carried > 0 && (
        <p className="text-sm text-orange-700 text-center">
          {summary.priorities_carried} prioridad(es) continúan la próxima semana
        </p>
      )}
    </div>
  );
}
