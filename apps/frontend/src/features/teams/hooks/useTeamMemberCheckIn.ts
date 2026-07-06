import { useQuery } from "@tanstack/react-query";
import { getTeamMemberCheckIn } from "../services/team-service";

export function useTeamMemberCheckIn(employeeId: string) {
  return useQuery({
    queryKey: ["teams", "member-checkin", employeeId],
    queryFn: () => getTeamMemberCheckIn(employeeId),
    enabled: !!employeeId,
    retry: (failureCount, error: any) => {
      if (error?.status === 404) return false;
      return failureCount < 2;
    },
  });
}
