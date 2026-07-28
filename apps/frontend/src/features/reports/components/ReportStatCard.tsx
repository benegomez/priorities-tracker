interface ReportStatCardProps {
  label: string;
  value: string | number;
  sublabel?: string;
}

export function ReportStatCard({ label, value, sublabel }: ReportStatCardProps) {
  return (
    <div className="rounded-lg border border-border bg-white px-5 py-4">
      <p className="text-sm text-secondary">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-gray-900">{value}</p>
      {sublabel && <p className="mt-0.5 text-xs text-secondary">{sublabel}</p>}
    </div>
  );
}
