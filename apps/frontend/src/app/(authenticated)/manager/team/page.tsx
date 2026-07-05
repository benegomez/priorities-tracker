import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ManagerTeamPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Vista de Equipo</h1>
      <Card>
        <CardHeader><CardTitle>Próximamente</CardTitle></CardHeader>
        <CardContent><p className="text-secondary">Vista de equipo con estado de check-ins y CRS.</p></CardContent>
      </Card>
    </div>
  );
}
