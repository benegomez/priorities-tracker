"use client";

export default function CheckOutError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="text-center p-6" role="alert">
      <h2 className="text-xl font-semibold text-danger">Algo salió mal</h2>
      <p className="text-secondary mt-2">{error.message}</p>
      <button onClick={reset} className="mt-4 rounded-lg bg-primary px-4 py-2 text-white hover:bg-primary-dark">
        Reintentar
      </button>
    </div>
  );
}
