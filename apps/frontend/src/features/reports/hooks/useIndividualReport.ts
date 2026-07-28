"use client";

import { useQuery } from "@tanstack/react-query";
import { getIndividualReport } from "../services/report-service";

export function useIndividualReport(weeks = 8) {
  return useQuery({
    queryKey: ["reports", "individual", weeks],
    queryFn: () => getIndividualReport(weeks),
  });
}
