"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import type { CRSCurrentResponse } from "../services/crs-service";

interface CRSScoreCardProps {
  crs: CRSCurrentResponse;
}

const riskColors: Record<string, string> = {
  low: "text-success",
  moderate: "text-accent",
  high: "text-danger",
};

const riskBadgeVariant: Record<string, "success" | "warning" | "danger"> = {
  low: "success",
  moderate: "warning",
  high: "danger",
};

function getScoreLabel(score: number): string {
  if (score >= 90) return "Excelente";
  if (score >= 75) return "Confiable";
  if (score >= 60) return "Riesgo Moderado";
  return "Riesgo Alto";
}

export function CRSScoreCard({ crs }: CRSScoreCardProps) {
  return (
    <Card>
      <CardContent className="p-6 text-center space-y-3">
        <p className="text-sm text-secondary">Commitment Reliability Score</p>
        <p className={`text-5xl font-bold ${riskColors[crs.risk_level]}`} aria-label={`Score: ${crs.score}`}>
          {crs.score.toFixed(1)}
        </p>
        <div className="flex items-center justify-center gap-2">
          <Badge variant={riskBadgeVariant[crs.risk_level]}>{getScoreLabel(crs.score)}</Badge>
        </div>
        <p className="text-xs text-secondary">
          Semana del {crs.week_start} · Fórmula {crs.formula_version}
        </p>

        {/* Detail */}
        <div className="grid grid-cols-2 gap-4 pt-3 border-t border-border text-sm">
          <div>
            <p className="text-secondary">Prioridades</p>
            <p className="font-medium">{crs.priorities_completed}/{crs.priorities_total} completadas</p>
          </div>
          <div>
            <p className="text-secondary">Tareas</p>
            <p className="font-medium">{crs.tasks_completed}/{crs.tasks_total} completadas</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
