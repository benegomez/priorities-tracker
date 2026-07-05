"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { CRSHistoryItem } from "../services/crs-service";

interface CRSHistoryChartProps {
  items: CRSHistoryItem[];
}

const trendArrows: Record<string, string> = {
  improving: "↑",
  stable: "→",
  declining: "↓",
};

const riskBadgeVariant: Record<string, "success" | "warning" | "danger"> = {
  low: "success",
  moderate: "warning",
  high: "danger",
};

export function CRSHistoryChart({ items }: CRSHistoryChartProps) {
  if (items.length === 0) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Historial</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-left text-secondary">
                <th className="pb-2 font-medium">Semana</th>
                <th className="pb-2 font-medium">Score</th>
                <th className="pb-2 font-medium">Tendencia</th>
                <th className="pb-2 font-medium">Riesgo</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.week_start} className="border-b border-border last:border-0">
                  <td className="py-2">{item.week_start}</td>
                  <td className="py-2 font-medium">{item.score.toFixed(1)}</td>
                  <td className="py-2">{trendArrows[item.trend]} {item.trend}</td>
                  <td className="py-2">
                    <Badge variant={riskBadgeVariant[item.risk_level]}>{item.risk_level}</Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}
