import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ManagerWeeklyPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Vista Semanal</h1>
      <Card>
        <CardHeader><CardTitle>Próximamente</CardTitle></CardHeader>
        <CardContent><p className="text-secondary">Resumen semanal del equipo con prioridades y riesgos.</p></CardContent>
      </Card>
    </div>
  );
}
