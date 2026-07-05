"use client";

export function CheckInLockedBanner() {
  return (
    <div className="rounded-lg border border-orange-200 bg-orange-50 p-4" role="alert">
      <p className="text-orange-800 font-medium">🔒 Check-In bloqueado</p>
      <p className="text-orange-700 text-sm mt-1">
        Este Check-In no puede editarse porque ya existe un Check-Out para esta semana.
      </p>
    </div>
  );
}
