import { z } from "zod";

export const createCheckOutSchema = z.object({
  checkin_id: z.string().uuid(),
});

export const submitCheckOutSchema = z.object({
  notes: z.string().max(2000).nullable().optional(),
  lessons_learned: z.string().max(2000).nullable().optional(),
});

export type SubmitCheckOutValues = z.infer<typeof submitCheckOutSchema>;
