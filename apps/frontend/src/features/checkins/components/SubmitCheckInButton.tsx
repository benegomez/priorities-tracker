"use client";

import { useState } from "react";
import { useSubmitCheckIn } from "../hooks/useSubmitCheckIn";
import type { ApiError } from "@/lib/api-client";

interface SubmitCheckInButtonProps {
  checkinId: string;
  prioritiesCount: number;
}

export function SubmitCheckInButton({ checkinId, prioritiesCount }: SubmitCheckInButtonProps) {
  const [showConfirm, setShowConfirm] = useState(false);
  const { mutate, isPending, error } = useSubmitCheckIn();
  const disabled = prioritiesCount === 0 || isPending;

  function handleConfirm() {
    mutate(checkinId);
    setShowConfirm(false);
  }

  const apiError = error as ApiError | null;

  return (
    <>
      <button
        onClick={() => setShowConfirm(true)}
        disabled={disabled}
        aria-disabled={disabled}
        className="rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Enviar Check-In
      </button>
      {disabled && prioritiesCount === 0 && (
        <p className="text-sm text-gray-500 mt-1">Agrega al menos una prioridad para enviar</p>
      )}
      {apiError && (
        <p className="text-sm text-red-600 mt-1" role="alert" aria-live="polite">
          {apiError.message}
        </p>
      )}

      {showConfirm && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
          role="dialog"
          aria-modal="true"
          aria-labelledby="confirm-title"
        >
          <div className="bg-white rounded-lg p-6 max-w-sm w-full mx-4 shadow-xl">
            <h3 id="confirm-title" className="text-lg font-semibold mb-2">
              Confirmar envío
            </h3>
            <p className="text-gray-600 mb-4">
              ¿Estás seguro de enviar tu Check-In con {prioritiesCount} prioridad(es)?
              No podrás agregar más prioridades después.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowConfirm(false)}
                className="rounded-md border px-3 py-1.5 text-sm hover:bg-gray-50"
                autoFocus
              >
                Cancelar
              </button>
              <button
                onClick={handleConfirm}
                className="rounded-md bg-green-600 px-3 py-1.5 text-sm text-white hover:bg-green-700"
              >
                Confirmar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
