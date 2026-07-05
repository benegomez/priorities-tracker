"use client";

interface CheckOutNotesProps {
  notes: string;
  lessonsLearned: string;
  onNotesChange: (value: string) => void;
  onLessonsChange: (value: string) => void;
  readOnly?: boolean;
}

export function CheckOutNotes({ notes, lessonsLearned, onNotesChange, onLessonsChange, readOnly = false }: CheckOutNotesProps) {
  return (
    <div className="space-y-4">
      <div>
        <label htmlFor="checkout-notes" className="block text-sm font-medium text-gray-700">
          Notas de la semana (opcional)
        </label>
        <textarea
          id="checkout-notes"
          value={notes}
          onChange={(e) => onNotesChange(e.target.value)}
          disabled={readOnly}
          className="mt-1 w-full rounded-lg border border-border px-3 py-2 text-sm disabled:bg-surface disabled:text-secondary"
          rows={3}
          placeholder="¿Algo relevante que quieras registrar?"
          maxLength={2000}
        />
      </div>
      <div>
        <label htmlFor="checkout-lessons" className="block text-sm font-medium text-gray-700">
          Lecciones aprendidas (opcional)
        </label>
        <textarea
          id="checkout-lessons"
          value={lessonsLearned}
          onChange={(e) => onLessonsChange(e.target.value)}
          disabled={readOnly}
          className="mt-1 w-full rounded-lg border border-border px-3 py-2 text-sm disabled:bg-surface disabled:text-secondary"
          rows={3}
          placeholder="¿Qué aprendiste esta semana?"
          maxLength={2000}
        />
      </div>
    </div>
  );
}
