"use client";

import { useCurrentCheckIn } from "@/features/checkins/hooks/useCurrentCheckIn";
import { useCreateCheckOut } from "../hooks/useCreateCheckOut";
import type { ApiError } from "@/lib/api-client";

export function CheckOutForm() {
  const { data: checkin } = useCurrentCheckIn();
  const { mutate, isPending, error } = useCreateCheckOut();

  const checkinSubmitted = checkin?.status === "submitted";
  const apiError = error as ApiError | null;

  function handleCreate() {
    if (checkin) mutate(checkin.id);
  }

  return (
    <div className="flex flex-col items-center gap-4 p-8">
      <h2 className="text-xl font-semibold">No tienes un Check-Out para esta semana</h2>
      {checkinSubmitted ? (
        <>
          <p className="text-secondary">Cierra tu semana registrando qué lograste completar.</p>
          <button
            onClick={handleCreate}
            disabled={isPending}
            className="rounded-lg bg-primary px-4 py-2 text-white hover:bg-primary-dark disabled:opacity-50"
            aria-label="Crear Check-Out semanal"
          >
            {isPending ? "Creando..." : "Crear Check-Out"}
          </button>
        </>
      ) : (
        <p className="text-secondary">Primero debes enviar tu Check-In para poder crear el Check-Out.</p>
      )}
      {apiError && (
        <p className="text-sm text-danger" role="alert" aria-live="polite">{apiError.message}</p>
      )}
    </div>
  );
}
