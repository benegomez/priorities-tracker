"use client";

interface TeamCRSBadgeProps {
  score: number;
  riskLevel: "low" | "moderate" | "high";
}

const riskColors = {
  low: "bg-green-100 text-green-800",
  moderate: "bg-orange-100 text-orange-800",
  high: "bg-red-100 text-red-800",
};

export function TeamCRSBadge({ score, riskLevel }: TeamCRSBadgeProps) {
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-sm font-semibold ${riskColors[riskLevel]}`} aria-label={`CRS: ${score.toFixed(1)}`}>
      {score.toFixed(1)}
    </span>
  );
}
