import { useQuery } from "@tanstack/react-query";
import { getMyTeam } from "../services/team-service";

export function useMyTeam() {
  return useQuery({
    queryKey: ["teams", "my-team"],
    queryFn: getMyTeam,
  });
}
