"use client";

import { Card, CardContent } from "@/components/ui/card";

export function CRSEmptyState() {
  return (
    <Card>
      <CardContent className="p-8 text-center">
        <p className="text-xl font-semibold text-gray-900">Aún no tienes un CRS calculado</p>
        <p className="text-secondary mt-2">Completa tu primer Check-Out para ver tu Commitment Reliability Score.</p>
      </CardContent>
    </Card>
  );
}
