"use client";

interface CRSTrendIndicatorProps {
  trend: "improving" | "stable" | "declining";
}

const trendConfig = {
  improving: { arrow: "↑", label: "Mejorando", className: "text-success" },
  stable: { arrow: "→", label: "Estable", className: "text-secondary" },
  declining: { arrow: "↓", label: "Declinando", className: "text-danger" },
};

export function CRSTrendIndicator({ trend }: CRSTrendIndicatorProps) {
  const config = trendConfig[trend];
  return (
    <div className={`flex items-center gap-1 ${config.className}`} aria-label={`Tendencia: ${config.label}`}>
      <span className="text-lg">{config.arrow}</span>
      <span className="text-sm font-medium">{config.label}</span>
    </div>
  );
}
