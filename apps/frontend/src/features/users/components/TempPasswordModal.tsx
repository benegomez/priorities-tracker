"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";

interface TempPasswordModalProps {
  email: string;
  password: string;
  onClose: () => void;
}

export function TempPasswordModal({ email, password, onClose }: TempPasswordModalProps) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(password);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" role="dialog" aria-modal="true">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-sm p-6 space-y-4">
        <div className="flex items-center gap-2 text-green-600">
          <Check className="h-5 w-5" />
          <h2 className="text-lg font-semibold">Usuario creado</h2>
        </div>

        <p className="text-sm text-gray-600">
          El usuario <span className="font-medium">{email}</span> fue creado exitosamente.
        </p>

        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-700">Contraseña temporal:</p>
          <div className="flex items-center gap-2 bg-gray-50 rounded-lg border border-gray-200 px-3 py-2">
            <code className="flex-1 text-sm font-mono tracking-wider">{password}</code>
            <button
              onClick={handleCopy}
              className="text-gray-500 hover:text-gray-700"
              aria-label="Copiar contraseña"
            >
              {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
            </button>
          </div>
          <p className="text-xs text-amber-600 bg-amber-50 rounded px-2 py-1">
            ⚠️ Guarda esta contraseña — no se mostrará nuevamente.
          </p>
        </div>

        <button
          onClick={onClose}
          className="w-full rounded-lg bg-primary px-4 py-2 text-sm text-white hover:bg-primary/90"
        >
          Entendido
        </button>
      </div>
    </div>
  );
}
