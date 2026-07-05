import { z } from "zod";

export const createCheckInSchema = z.object({
  week_start: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Formato YYYY-MM-DD requerido"),
});

export type CreateCheckInValues = z.infer<typeof createCheckInSchema>;
