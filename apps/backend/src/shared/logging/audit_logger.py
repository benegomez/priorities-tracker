import logging
import json
from datetime import datetime, timezone
from uuid import UUID

logger = logging.getLogger("audit")


def emit_audit_event(
    event: str,
    *,
    user_id: UUID | str | None = None,
    organization_id: UUID | str | None = None,
    correlation_id: str | None = None,
    metadata: dict | None = None,
) -> None:
    entry = {
        "event": event,
        "user_id": str(user_id) if user_id else None,
        "organization_id": str(organization_id) if organization_id else None,
        "correlation_id": correlation_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
    }
    logger.info(json.dumps(entry))
