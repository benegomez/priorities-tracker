"use client";

import { useState } from "react";
import { useResubmitCheckIn } from "../hooks/useResubmitCheckIn";
import type { ApiError } from "@/lib/api-client";

interface ResubmitButtonProps {
  checkinId: string;
  newPrioritiesCount: number;
}

export function ResubmitButton({ checkinId, newPrioritiesCount }: ResubmitButtonProps) {
  const [showConfirm, setShowConfirm] = useState(false);
  const { mutate, isPending, error } = useResubmitCheckIn();
  const apiError = error as ApiError | null;

  if (newPrioritiesCount === 0) return null;

  function handleConfirm() {
    mutate(checkinId);
    setShowConfirm(false);
  }

  return (
    <>
      <button
        onClick={() => setShowConfirm(true)}
        disabled={isPending}
        className="rounded-lg bg-primary px-4 py-2 text-white hover:bg-primary-dark disabled:opacity-50 transition-colors"
      >
        {isPending ? "Actualizando..." : "Actualizar Check-In"}
      </button>
      {apiError && (
        <p className="text-sm text-danger mt-1" role="alert">{apiError.message}</p>
      )}

      {showConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true" aria-labelledby="resubmit-title">
          <div className="bg-white rounded-xl p-6 max-w-sm w-full mx-4 shadow-xl">
            <h3 id="resubmit-title" className="text-lg font-semibold mb-2">Actualizar Check-In</h3>
            <p className="text-secondary mb-4">
              ¿Confirmas agregar {newPrioritiesCount} nueva(s) prioridad(es) a tu Check-In?
            </p>
            <div className="flex gap-3 justify-end">
              <button onClick={() => setShowConfirm(false)} className="rounded-lg border border-border px-3 py-1.5 text-sm hover:bg-surface">
                Cancelar
              </button>
              <button onClick={handleConfirm} className="rounded-lg bg-primary px-3 py-1.5 text-sm text-white hover:bg-primary-dark">
                Confirmar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
