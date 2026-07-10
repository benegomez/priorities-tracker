"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { TeamSummaryResponse } from "../services/ai-service";

interface AISummaryCardProps {
  data: TeamSummaryResponse;
  onRegenerate: () => void;
  isRegenerating: boolean;
}

function OriginBadge({ fallback, cached }: { fallback: boolean; cached: boolean }) {
  if (fallback) {
    return <Badge variant="outline">Resumen automático (sin IA)</Badge>;
  }
  if (cached) {
    return <Badge variant="info">Desde cache</Badge>;
  }
  return <Badge variant="success">Generado por IA</Badge>;
}

export function AISummaryCard({ data, onRegenerate, isRegenerating }: AISummaryCardProps) {
  const { summary, generated_at, model, data_snapshot, fallback, cached } = data;

  return (
    <div className="space-y-4">
      {/* Origin + Regenerate */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <OriginBadge fallback={fallback} cached={cached} />
          {model && <span className="text-xs text-secondary">Modelo: {model}</span>}
        </div>
        <button
          onClick={onRegenerate}
          disabled={isRegenerating}
          className="text-sm text-primary hover:underline disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isRegenerating ? "Regenerando..." : "Regenerar"}
        </button>
      </div>

      {/* Summary */}
      <Card>
        <CardContent className="p-6">
          <div className="prose prose-sm max-w-none whitespace-pre-line" role="article" aria-label="Resumen semanal del equipo">
            {summary}
          </div>
        </CardContent>
      </Card>

      {/* Metrics */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Métricas de la semana</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold">{data_snapshot.team_size}</p>
              <p className="text-xs text-secondary">Miembros</p>
            </div>
            <div>
              <p className="text-2xl font-bold">{data_snapshot.avg_crs.toFixed(1)}</p>
              <p className="text-xs text-secondary">CRS Promedio</p>
            </div>
            <div>
              <p className="text-2xl font-bold">{data_snapshot.completion_rate.toFixed(0)}%</p>
              <p className="text-xs text-secondary">Cumplimiento</p>
            </div>
            <div>
              <p className="text-2xl font-bold">{data_snapshot.completed_priorities}/{data_snapshot.total_priorities}</p>
              <p className="text-xs text-secondary">Prioridades</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Timestamp */}
      <p className="text-xs text-secondary text-right">
        Generado: {new Date(generated_at).toLocaleString("es")}
      </p>
    </div>
  );
}
