"use client";

import { Sparkles } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

interface AISummaryEmptyStateProps {
  onGenerate: () => void;
  isLoading: boolean;
}

export function AISummaryEmptyState({ onGenerate, isLoading }: AISummaryEmptyStateProps) {
  return (
    <Card>
      <CardContent className="p-8 text-center space-y-4">
        <Sparkles className="h-10 w-10 text-primary mx-auto" />
        <p className="text-lg font-semibold text-gray-900">Resumen Semanal con IA</p>
        <p className="text-sm text-secondary max-w-md mx-auto">
          Genera un resumen ejecutivo de tu equipo. Incluye logros, puntos de atención y recomendaciones basadas en los datos de la semana.
        </p>
        <button
          onClick={onGenerate}
          disabled={isLoading}
          aria-busy={isLoading}
          className="inline-flex items-center gap-2 rounded-md bg-primary px-5 py-2.5 text-sm font-medium text-white hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Sparkles className="h-4 w-4" />
          {isLoading ? "Generando resumen..." : "Generar Resumen"}
        </button>
      </CardContent>
    </Card>
  );
}
