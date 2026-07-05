"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { useProjectDetail } from "@/features/projects/hooks/useProjectDetail";
import { useUpdateProject, useCreatePhase, useUpdatePhase, useAddMember, useRemoveMember } from "@/features/projects/hooks/useProjectMutations";
import { useOrgMembers } from "@/features/projects/hooks/useOrgMembers";
import { UserSelect } from "@/features/projects/components/UserSelect";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const PROJECT_TRANSITIONS: Record<string, string[]> = {
  draft: ["active"],
  active: ["on_hold", "completed"],
  on_hold: ["active"],
  completed: ["archived"],
  archived: [],
};

const PHASE_TRANSITIONS: Record<string, string[]> = {
  planned: ["active", "cancelled"],
  active: ["completed", "cancelled"],
  completed: [],
  cancelled: [],
};

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: project, isLoading } = useProjectDetail(id);
  const { data: orgMembers = [] } = useOrgMembers();
  const updateProject = useUpdateProject(id);
  const createPhase = useCreatePhase(id);
  const updatePhase = useUpdatePhase(id);
  const addMember = useAddMember(id);
  const removeMember = useRemoveMember(id);

  const [newPhaseName, setNewPhaseName] = useState("");
  const [selectedMemberId, setSelectedMemberId] = useState("");

  if (isLoading || !project) {
    return <div className="space-y-4 animate-pulse"><div className="h-8 w-48 bg-gray-200 rounded-lg" /><div className="h-32 bg-gray-200 rounded-lg" /></div>;
  }

  const validTransitions = PROJECT_TRANSITIONS[project.status] ?? [];
  const existingMemberIds = project.members.map((m) => m.user_id);

  function handleAddMember(userId: string) {
    if (!userId) return;
    addMember.mutate(userId);
    setSelectedMemberId("");
  }

  return (
    <div className="space-y-6">
      <header>
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold text-gray-900">{project.name}</h1>
          <Badge variant={project.status === "active" ? "success" : "outline"}>{project.status}</Badge>
        </div>
        {project.description && <p className="text-secondary text-sm mt-1">{project.description}</p>}
        <div className="flex items-center gap-2 mt-2">
          <span className="text-sm text-gray-700">Responsable:</span>
          <UserSelect
            users={orgMembers}
            value={project.owner?.id ?? ""}
            onChange={(userId) => updateProject.mutate({ owner_id: userId })}
            placeholder="Selecciona responsable..."
          />
        </div>
      </header>

      {/* Status transitions */}
      {validTransitions.length > 0 && (
        <div className="flex gap-2">
          {validTransitions.map((s) => (
            <button key={s} onClick={() => updateProject.mutate({ status: s })} className="rounded-lg border border-border px-3 py-1.5 text-xs hover:bg-primary-light hover:text-primary transition-colors">
              → {s}
            </button>
          ))}
        </div>
      )}

      {/* Phases */}
      <Card>
        <CardHeader><CardTitle>Fases</CardTitle></CardHeader>
        <CardContent className="space-y-2">
          {project.phases.map((phase) => (
            <div key={phase.id} className="flex items-center justify-between rounded-lg border border-border p-3">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">{phase.name}</span>
                <Badge variant="outline">{phase.status}</Badge>
              </div>
              <div className="flex gap-1">
                {(PHASE_TRANSITIONS[phase.status] ?? []).map((s) => (
                  <button key={s} onClick={() => updatePhase.mutate({ phaseId: phase.id, data: { status: s } })} className="rounded border px-2 py-0.5 text-xs text-secondary hover:text-primary">
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ))}
          <form onSubmit={(e) => { e.preventDefault(); if (newPhaseName.trim()) { createPhase.mutate(newPhaseName.trim()); setNewPhaseName(""); } }} className="flex gap-2 pt-2">
            <input value={newPhaseName} onChange={(e) => setNewPhaseName(e.target.value)} placeholder="Nueva fase..." className="flex-1 rounded-lg border border-border px-3 py-1.5 text-sm" />
            <button type="submit" disabled={!newPhaseName.trim()} className="rounded-lg bg-primary px-3 py-1.5 text-sm text-white disabled:opacity-50">Agregar</button>
          </form>
        </CardContent>
      </Card>

      {/* Members */}
      <Card>
        <CardHeader><CardTitle>Participantes</CardTitle></CardHeader>
        <CardContent className="space-y-2">
          {project.members.map((member) => (
            <div key={member.user_id} className="flex items-center justify-between rounded-lg border border-border p-3">
              <div>
                <span className="text-sm font-medium">{member.full_name}</span>
                <Badge variant="outline" className="ml-2">{member.role}</Badge>
              </div>
              <button onClick={() => removeMember.mutate(member.user_id)} className="text-xs text-danger hover:underline">Remover</button>
            </div>
          ))}
          {project.members.length === 0 && <p className="text-secondary text-sm">Sin participantes.</p>}

          {/* Add member select */}
          <div className="pt-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Agregar participante</label>
            <UserSelect
              users={orgMembers}
              value={selectedMemberId}
              onChange={handleAddMember}
              placeholder="Selecciona un usuario para agregar..."
              excludeIds={existingMemberIds}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
