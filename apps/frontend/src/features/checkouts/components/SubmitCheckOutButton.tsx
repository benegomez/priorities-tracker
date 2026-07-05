"use client";

import { useState } from "react";
import { useSubmitCheckOut } from "../hooks/useSubmitCheckOut";
import type { ApiError } from "@/lib/api-client";

interface SubmitCheckOutButtonProps {
  checkoutId: string;
  notes: string;
  lessonsLearned: string;
}

export function SubmitCheckOutButton({ checkoutId, notes, lessonsLearned }: SubmitCheckOutButtonProps) {
  const [showConfirm, setShowConfirm] = useState(false);
  const { mutate, isPending, error } = useSubmitCheckOut();
  const apiError = error as ApiError | null;

  function handleConfirm() {
    mutate({ id: checkoutId, notes, lessonsLearned });
    setShowConfirm(false);
  }

  return (
    <>
      <button
        onClick={() => setShowConfirm(true)}
        disabled={isPending}
        className="rounded-lg bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:opacity-50"
      >
        Enviar Check-Out
      </button>
      {apiError && (
        <p className="text-sm text-danger mt-1" role="alert" aria-live="polite">{apiError.message}</p>
      )}

      {showConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" role="dialog" aria-modal="true" aria-labelledby="confirm-checkout-title">
          <div className="bg-white rounded-xl p-6 max-w-sm w-full mx-4 shadow-xl">
            <h3 id="confirm-checkout-title" className="text-lg font-semibold mb-2">Confirmar envío</h3>
            <p className="text-secondary mb-4">
              ¿Estás seguro de enviar tu Check-Out? Las prioridades no marcadas pasarán a carry-over.
            </p>
            <div className="flex gap-3 justify-end">
              <button onClick={() => setShowConfirm(false)} className="rounded-lg border border-border px-3 py-1.5 text-sm hover:bg-surface">
                Cancelar
              </button>
              <button onClick={handleConfirm} className="rounded-lg bg-green-600 px-3 py-1.5 text-sm text-white hover:bg-green-700">
                Confirmar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
