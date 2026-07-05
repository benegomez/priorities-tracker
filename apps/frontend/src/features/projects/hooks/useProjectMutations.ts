"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createProject, updateProject, createPhase, updatePhase, addMember, removeMember } from "../services/project-service";

export function useCreateProject() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { name: string; description?: string; owner_id: string }) => createProject(data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["projects"] }); },
  });
}

export function useUpdateProject(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { name?: string; description?: string; owner_id?: string; status?: string }) => updateProject(id, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["projects"] }); },
  });
}

export function useCreatePhase(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (name: string) => createPhase(projectId, name),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["projects", projectId] }); },
  });
}

export function useUpdatePhase(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ phaseId, data }: { phaseId: string; data: { name?: string; status?: string } }) => updatePhase(projectId, phaseId, data),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["projects", projectId] }); },
  });
}

export function useAddMember(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (userId: string) => addMember(projectId, userId),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["projects", projectId] }); },
  });
}

export function useRemoveMember(projectId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (userId: string) => removeMember(projectId, userId),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["projects", projectId] }); },
  });
}
