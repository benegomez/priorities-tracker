"use client";

import { useState } from "react";
import { useCreatePriority } from "../hooks/useCreatePriority";
import { useAvailablePhases } from "@/features/projects/hooks/useAvailablePhases";
import type { ApiError } from "@/lib/api-client";
import type { PriorityResponse } from "../services/priority-service";

interface PriorityFormProps {
  checkinId: string;
  onPriorityCreated?: (priority: PriorityResponse) => void;
}

export function PriorityForm({ checkinId, onPriorityCreated }: PriorityFormProps) {
  const [phaseId, setPhaseId] = useState("");
  const [title, setTitle] = useState("");
  const [level, setLevel] = useState<"low" | "medium" | "high">("medium");
  const [description, setDescription] = useState("");
  const { mutate, isPending, error } = useCreatePriority(checkinId);
  const { data: phases = [], isLoading: phasesLoading } = useAvailablePhases();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !phaseId) return;
    mutate(
      {
        checkin_id: checkinId,
        phase_id: phaseId,
        title: title.trim(),
        description: description.trim() || null,
        priority_level: level,
      },
      {
        onSuccess: (data) => {
          setTitle("");
          setDescription("");
          onPriorityCreated?.(data as unknown as PriorityResponse);
        },
      }
    );
  }

  const apiError = error as ApiError | null;

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-border p-4 space-y-3 bg-surface">
      <h3 className="font-medium text-sm">Agregar Prioridad</h3>

      <div>
        <label htmlFor="phase-select" className="block text-sm font-medium text-gray-700">
          Fase del proyecto
        </label>
        <select
          id="phase-select"
          value={phaseId}
          onChange={(e) => setPhaseId(e.target.value)}
          className="mt-1 w-full rounded-lg border border-border px-3 py-2 text-sm"
          required
          disabled={phasesLoading}
        >
          <option value="">{phasesLoading ? "Cargando fases..." : "Selecciona una fase..."}</option>
          {phases.map((phase) => (
            <option key={phase.id} value={phase.id}>
              {phase.project_name} → {phase.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="priority-title" className="block text-sm font-medium text-gray-700">
          Título
        </label>
        <input
          id="priority-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="mt-1 w-full rounded-lg border border-border px-3 py-2 text-sm"
          placeholder="¿Qué te comprometes a lograr?"
          maxLength={255}
          required
        />
      </div>

      <div>
        <label htmlFor="priority-description" className="block text-sm font-medium text-gray-700">
          Descripción (opcional)
        </label>
        <textarea
          id="priority-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="mt-1 w-full rounded-lg border border-border px-3 py-2 text-sm"
          rows={2}
          maxLength={1000}
        />
      </div>

      <div>
        <label htmlFor="priority-level" className="block text-sm font-medium text-gray-700">
          Nivel de prioridad
        </label>
        <select
          id="priority-level"
          value={level}
          onChange={(e) => setLevel(e.target.value as "low" | "medium" | "high")}
          className="mt-1 w-full rounded-lg border border-border px-3 py-2 text-sm"
        >
          <option value="high">Alta</option>
          <option value="medium">Media</option>
          <option value="low">Baja</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={isPending || !title.trim() || !phaseId}
        className="rounded-lg bg-primary px-4 py-2 text-sm text-white hover:bg-primary-dark disabled:opacity-50"
      >
        {isPending ? "Agregando..." : "Agregar Prioridad"}
      </button>

      {apiError && (
        <p className="text-sm text-danger" role="alert" aria-live="polite">
          {apiError.message}
        </p>
      )}
    </form>
  );
}
