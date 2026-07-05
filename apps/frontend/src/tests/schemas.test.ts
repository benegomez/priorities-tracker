import { describe, it, expect } from "vitest";
import { createCheckInSchema } from "@/features/checkins/schemas/checkin-schema";
import { createPrioritySchema } from "@/features/priorities/schemas/priority-schema";
import { createTaskSchema } from "@/features/priorities/schemas/task-schema";

describe("createCheckInSchema", () => {
  it("accepts valid date", () => {
    const result = createCheckInSchema.safeParse({ week_start: "2025-01-06" });
    expect(result.success).toBe(true);
  });

  it("rejects invalid date format", () => {
    const result = createCheckInSchema.safeParse({ week_start: "01-06-2025" });
    expect(result.success).toBe(false);
  });

  it("rejects empty string", () => {
    const result = createCheckInSchema.safeParse({ week_start: "" });
    expect(result.success).toBe(false);
  });
});

describe("createPrioritySchema", () => {
  const validData = {
    checkin_id: "11111111-1111-1111-1111-111111111111",
    phase_id: "22222222-2222-2222-2222-222222222222",
    title: "Implement feature",
    priority_level: "high" as const,
  };

  it("accepts valid data", () => {
    const result = createPrioritySchema.safeParse(validData);
    expect(result.success).toBe(true);
  });

  it("rejects empty title", () => {
    const result = createPrioritySchema.safeParse({ ...validData, title: "" });
    expect(result.success).toBe(false);
  });

  it("rejects invalid UUID for phase_id", () => {
    const result = createPrioritySchema.safeParse({ ...validData, phase_id: "not-a-uuid" });
    expect(result.success).toBe(false);
  });

  it("rejects invalid priority_level", () => {
    const result = createPrioritySchema.safeParse({ ...validData, priority_level: "critical" });
    expect(result.success).toBe(false);
  });
});

describe("createTaskSchema", () => {
  it("accepts valid title", () => {
    const result = createTaskSchema.safeParse({ title: "Write tests" });
    expect(result.success).toBe(true);
  });

  it("rejects empty title", () => {
    const result = createTaskSchema.safeParse({ title: "" });
    expect(result.success).toBe(false);
  });

  it("accepts optional description", () => {
    const result = createTaskSchema.safeParse({ title: "Task", description: "Details" });
    expect(result.success).toBe(true);
  });
});
