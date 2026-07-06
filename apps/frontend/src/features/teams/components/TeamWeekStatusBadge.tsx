"use client";

interface TeamWeekStatusBadgeProps {
  status: "draft" | "submitted" | null;
  label: string;
}

const statusConfig = {
  submitted: { text: "Enviado", className: "bg-green-100 text-green-800" },
  draft: { text: "Borrador", className: "bg-yellow-100 text-yellow-800" },
  null: { text: "Sin crear", className: "bg-gray-100 text-gray-500" },
};

export function TeamWeekStatusBadge({ status, label }: TeamWeekStatusBadgeProps) {
  const config = statusConfig[status ?? "null"];
  return (
    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${config.className}`} aria-label={`${label}: ${config.text}`}>
      {config.text}
    </span>
  );
}
