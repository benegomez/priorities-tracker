"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useProjects } from "@/features/projects/hooks/useProjects";
import { useCreateProject } from "@/features/projects/hooks/useProjectMutations";
import { useOrgMembers } from "@/features/projects/hooks/useOrgMembers";
import { UserSelect } from "@/features/projects/components/UserSelect";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

const statusVariant: Record<string, "default" | "success" | "warning" | "danger" | "outline"> = {
  draft: "outline",
  active: "success",
  on_hold: "warning",
  completed: "default",
  archived: "danger",
};

export default function ProjectsPage() {
  const router = useRouter();
  const { data, isLoading } = useProjects();
  const { data: orgMembers = [] } = useOrgMembers();
  const createMutation = useCreateProject();
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [ownerId, setOwnerId] = useState("");

  function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || !ownerId) return;
    createMutation.mutate(
      { name: name.trim(), description: description.trim() || undefined, owner_id: ownerId },
      { onSuccess: () => { setShowForm(false); setName(""); setDescription(""); setOwnerId(""); } }
    );
  }

  if (isLoading) {
    return <div className="space-y-4 animate-pulse"><div className="h-8 w-48 bg-gray-200 rounded-lg" /><div className="h-24 bg-gray-200 rounded-lg" /></div>;
  }

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Proyectos</h1>
        <button onClick={() => setShowForm(!showForm)} className="rounded-lg bg-primary px-4 py-2 text-sm text-white hover:bg-primary-dark">
          + Nuevo Proyecto
        </button>
      </header>

      {showForm && (
        <Card>
          <CardContent className="p-4">
            <form onSubmit={handleCreate} className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nombre del proyecto</label>
                <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Nombre del proyecto" className="w-full rounded-lg border border-border px-3 py-2 text-sm" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Descripción (opcional)</label>
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Descripción del proyecto" className="w-full rounded-lg border border-border px-3 py-2 text-sm" rows={2} />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Responsable</label>
                <UserSelect users={orgMembers} value={ownerId} onChange={setOwnerId} placeholder="Selecciona el responsable..." />
              </div>
              <div className="flex gap-2">
                <button type="submit" disabled={createMutation.isPending || !ownerId} className="rounded-lg bg-primary px-3 py-1.5 text-sm text-white disabled:opacity-50">Crear</button>
                <button type="button" onClick={() => setShowForm(false)} className="rounded-lg border border-border px-3 py-1.5 text-sm">Cancelar</button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="space-y-3">
        {data?.items.map((project) => (
          <Card key={project.id} className="cursor-pointer hover:border-primary transition-colors" onClick={() => router.push(`/admin/projects/${project.id}`)}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">{project.name}</p>
                  <p className="text-xs text-secondary mt-1">
                    {project.phases_count} fase(s) · {project.members_count} miembro(s)
                    {project.owner && ` · Owner: ${project.owner.full_name}`}
                  </p>
                </div>
                <Badge variant={statusVariant[project.status] ?? "outline"}>{project.status}</Badge>
              </div>
            </CardContent>
          </Card>
        ))}
        {data?.items.length === 0 && <p className="text-secondary text-sm">No hay proyectos creados.</p>}
      </div>
    </div>
  );
}
