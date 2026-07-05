"use client";

interface CheckInStatusProps {
  status: "draft" | "submitted" | "closed";
}

const statusConfig = {
  draft: { label: "Borrador", className: "bg-yellow-100 text-yellow-800" },
  submitted: { label: "Enviado", className: "bg-green-100 text-green-800" },
  closed: { label: "Cerrado", className: "bg-gray-100 text-gray-800" },
};

export function CheckInStatus({ status }: CheckInStatusProps) {
  const config = statusConfig[status];
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${config.className}`}>
      {config.label}
    </span>
  );
}
