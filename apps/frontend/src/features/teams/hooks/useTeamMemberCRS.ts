import { useQuery } from "@tanstack/react-query";
import { getTeamMemberCRS } from "../services/team-service";

export function useTeamMemberCRS(employeeId: string) {
  return useQuery({
    queryKey: ["teams", "member-crs", employeeId],
    queryFn: () => getTeamMemberCRS(employeeId),
    enabled: !!employeeId,
  });
}
