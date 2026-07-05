import { z } from "zod";

export const createPrioritySchema = z.object({
  checkin_id: z.string().uuid(),
  phase_id: z.string().uuid("Selecciona una fase"),
  title: z.string().min(1, "El título es requerido").max(255),
  description: z.string().max(1000).nullable().optional(),
  priority_level: z.enum(["low", "medium", "high"]),
});

export type CreatePriorityValues = z.infer<typeof createPrioritySchema>;
