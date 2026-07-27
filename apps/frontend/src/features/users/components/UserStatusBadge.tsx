import { Badge } from "@/components/ui/badge";

interface UserStatusBadgeProps {
  status: "active" | "inactive";
}

export function UserStatusBadge({ status }: UserStatusBadgeProps) {
  return (
    <Badge variant={status === "active" ? "success" : "danger"}>
      {status === "active" ? "Activo" : "Inactivo"}
    </Badge>
  );
}
