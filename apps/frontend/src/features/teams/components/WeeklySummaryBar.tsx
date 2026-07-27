"use client";

interface WeeklySummaryBarProps {
  total: number;
  checkins: number;
  checkouts: number;
}

export function WeeklySummaryBar({ total, checkins, checkouts }: WeeklySummaryBarProps) {
  return (
    <div className="flex items-center gap-6 rounded-lg border border-border bg-white px-5 py-3 text-sm">
      <span className="font-medium text-gray-700">Resumen semanal</span>
      <span className="text-secondary">
        Check-Ins: <span className="font-semibold text-gray-900">{checkins}/{total}</span>
      </span>
      <span className="text-secondary">
        Check-Outs: <span className="font-semibold text-gray-900">{checkouts}/{total}</span>
      </span>
    </div>
  );
}
