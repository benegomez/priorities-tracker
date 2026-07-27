import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { type TeamCreate, type TeamUpdate, teamAdminService } from "../services/team-service";

export function useAdminTeams(filters?: { page?: number }) {
  return useQuery({
    queryKey: ["admin-teams", filters],
    queryFn: () => teamAdminService.list(filters),
  });
}

export function useTeamDetail(id: string | null) {
  return useQuery({
    queryKey: ["admin-teams", id],
    queryFn: () => teamAdminService.getDetail(id!),
    enabled: !!id,
  });
}

export function useCreateTeam() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: TeamCreate) => teamAdminService.create(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin-teams"] }),
  });
}

export function useUpdateTeam() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: TeamUpdate }) =>
      teamAdminService.update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin-teams"] }),
  });
}

export function useAddMember() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ teamId, userId }: { teamId: string; userId: string }) =>
      teamAdminService.addMember(teamId, userId),
    onSuccess: (_data, { teamId }) =>
      queryClient.invalidateQueries({ queryKey: ["admin-teams", teamId] }),
  });
}

export function useRemoveMember() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ teamId, userId }: { teamId: string; userId: string }) =>
      teamAdminService.removeMember(teamId, userId),
    onSuccess: (_data, { teamId }) =>
      queryClient.invalidateQueries({ queryKey: ["admin-teams", teamId] }),
  });
}
