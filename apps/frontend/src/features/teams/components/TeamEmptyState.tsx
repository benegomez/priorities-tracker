"use client";

import { Card, CardContent } from "@/components/ui/card";

export function TeamEmptyState() {
  return (
    <Card>
      <CardContent className="py-12 text-center">
        <p className="text-lg font-medium text-gray-700">No tienes miembros en tu equipo</p>
        <p className="mt-1 text-sm text-secondary">Los empleados asignados a ti aparecerán aquí</p>
      </CardContent>
    </Card>
  );
}
